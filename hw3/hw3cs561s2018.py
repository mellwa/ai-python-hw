import numpy as np


class InputInfo:
    def __init__(self):
        self.__grid_row = None
        self.__grid_col = None
        self.__walls = []
        self.__terminals = []
        self.__walk_probability = None
        self.__run_probability = None
        self.__walk_reward = None
        self.__run_reward = None
        self.__discount_factor = None

    def set_grid_row(self, num):
        num = int(num)
        self.__grid_row = num

    def get_grid_row(self):
        return self.__grid_row

    def set_grid_col(self, num):
        num = int(num)
        self.__grid_col = num

    def get_grid_col(self):
        return self.__grid_col

    def add_wall(self, wall):
        wall[0] = int(wall[0])
        wall[1] = int(wall[1])
        self.__walls.append(wall)

    def get_walls(self):
        return self.__walls

    def add_terminal(self, terminal):
        terminal[0] = int(terminal[0])
        terminal[1] = int(terminal[1])
        terminal[2] = float(terminal[2])
        self.__terminals.append(terminal)

    def get_terminals(self):
        return self.__terminals

    def set_walk_probability(self, p):
        p = float(p)
        self.__walk_probability = p

    def get_walk_probability(self):
        return self.__walk_probability

    def set_run_probability(self, p):
        p = float(p)
        self.__run_probability = p

    def get_run_probability(self):
        return self.__run_probability

    def set_walk_reward(self, r):
        r = float(r)
        self.__walk_reward = r

    def get_walk_reward(self):
        return self.__walk_reward

    def set_run_reward(self, r):
        r = float(r)
        self.__run_reward = r

    def get_run_reward(self):
        return self.__run_reward

    def set_discount_factor(self, f):
        f = float(f)
        self.__discount_factor = f

    def get_discount_factor(self):
        return self.__discount_factor


class FileIO:
    def __init__(self):
        self.__input_file = 'input.txt'
        self.__input_info = InputInfo()

    def read(self):
        file_obj = open(self.__input_file, 'r+')
        line = ' '
        section_num = 1
        while line and section_num < 7:
            line = file_obj.readline()
            if section_num == 1:
                row_col = line.rstrip().split(',')
                if len(row_col) is not 2:
                    raise Exception('wrong raw and col input')
                self.__input_info.set_grid_row(row_col[0])
                self.__input_info.set_grid_col(row_col[1])
            if section_num == 2:
                wall_num = int(line.rstrip())
                for i in range(wall_num):
                    line = file_obj.readline()
                    wall = line.rstrip().split(',')
                    if len(wall) is not 2:
                        raise Exception('wrong wall position')
                    self.__input_info.add_wall(wall)
            if section_num == 3:  # terminals
                terminal_num = int(line.rstrip())
                for i in range(terminal_num):
                    line = file_obj.readline()
                    terminal = line.rstrip().split(',')
                    if len(terminal) is not 3:
                        raise Exception('wrong terminal position')
                    self.__input_info.add_terminal(terminal)
            if section_num == 4:  # probabilities
                probabilities = line.rstrip().split(',')
                if len(probabilities) is not 2:
                    raise Exception('wrong probabilies number')
                self.__input_info.set_walk_probability(probabilities[0])
                self.__input_info.set_run_probability(probabilities[1])
            if section_num == 5:  # rewards
                rewards = line.rstrip().split(',')
                if len(rewards) is not 2:
                    raise Exception('wrong rewards number')
                self.__input_info.set_walk_reward(rewards[0])
                self.__input_info.set_run_reward(rewards[1])
            if section_num == 6:  # discount factor
                factor = line.rstrip()
                self.__input_info.set_discount_factor(factor)
            section_num += 1
        file_obj.close()

    def get_input(self):
        return self.__input_info

    def write_to_file(self, output_str):
        output_file = open('output.txt', 'w+')
        output_file.write(output_str)
        output_file.close()


class VectorSolution:
    def __init__(self):
        self.__file_io = FileIO()
        self.__file_io.read()
        self.__input = self.__file_io.get_input()
        # self.__discount_factor = np.float128(self.__input.get_discount_factor())
        self.__discount_factor = self.__input.get_discount_factor()
        self.__utility = np.zeros((self.__input.get_grid_row(), self.__input.get_grid_col()))
        self.__policy = np.zeros((self.__input.get_grid_row(), self.__input.get_grid_col()))
        self.__run_reward = self.__input.get_run_reward()
        self.__walk_reward = self.__input.get_walk_reward()
        self.__run_probability = self.__input.get_run_probability()
        self.__walk_probability = self.__input.get_walk_probability()
        self.iterations = 0
        # self.__epsilon = np.float128(pow(self.__discount_factor, 1100))
        self.__epsilon = 0
        self.__row = self.__input.get_grid_row()
        self.__col = self.__input.get_grid_col()

        for terminal in self.__input.get_terminals():
            terminal[0] = self.__row - terminal[0]
            terminal[1] = terminal[1] - 1
            self.__utility[terminal[0], terminal[1]] = terminal[2]
            self.__policy[terminal[0], terminal[1]] = -2
        self.__terminals = np.where(self.__policy == -2)

        for wall in self.__input.get_walls():
            wall[0] = self.__row - wall[0]
            wall[1] = wall[1] - 1
            self.__utility[wall[0], wall[1]] = np.nan
            self.__policy[wall[0], wall[1]] = -1
        self.__walls = np.where(np.isnan(self.__utility))

        self.__action_map = {-2: 'Exit', -1: 'None', 0: 'Walk Up', 1: 'Walk Down', 2: 'Walk Left', 3: 'Walk Right',
                             4: 'Run Up', 5: 'Run Down', 6: 'Run Left', 7: 'Run Right'}

    def up_utility(self):
        walk_up_utility = np.vstack((self.__utility[0], np.delete(self.__utility, self.__row - 1, axis=0)))
        wall_indices = np.where(np.isnan(walk_up_utility))
        run_up_utility = np.vstack((self.__utility[1], np.delete(self.__utility, self.__row - 1, axis=0)))
        run_up_utility = np.vstack((self.__utility[0], np.delete(run_up_utility, self.__row - 1, axis=0)))
        run_up_utility[wall_indices] = np.nan
        walk_up_utility[wall_indices] = self.__utility[wall_indices]
        wall_indices = np.where(np.isnan(run_up_utility))
        run_up_utility[wall_indices] = self.__utility[wall_indices]
        return walk_up_utility, run_up_utility

    def down_utility(self):
        walk_down_utility = np.vstack((np.delete(self.__utility, 0, axis=0), self.__utility[self.__row - 1]))
        wall_indices = np.where(np.isnan(walk_down_utility))
        run_down_utility = np.vstack((np.delete(self.__utility, 0, axis=0), self.__utility[self.__row - 2]))
        run_down_utility = np.vstack((np.delete(run_down_utility, 0, axis=0), self.__utility[self.__row - 1]))
        run_down_utility[wall_indices] = np.nan
        walk_down_utility[wall_indices] = self.__utility[wall_indices]
        wall_indices = np.where(np.isnan(run_down_utility))
        run_down_utility[wall_indices] = self.__utility[wall_indices]
        return walk_down_utility, run_down_utility

    def left_utility(self):
        first_col = self.__utility[:, 0]
        first_col = first_col.reshape(len(first_col), 1)
        second_col = self.__utility[:, 1]
        second_col = second_col.reshape(len(first_col), 1)
        walk_left_utility = np.hstack((first_col, np.delete(self.__utility, self.__col - 1, axis=1)))
        run_left_utility = np.hstack((second_col, np.delete(self.__utility, self.__col - 1, axis=1)))
        run_left_utility = np.hstack((first_col, np.delete(run_left_utility, self.__col - 1, axis=1)))
        wall_indices = np.where(np.isnan(walk_left_utility))
        run_left_utility[wall_indices] = np.nan
        walk_left_utility[wall_indices] = self.__utility[wall_indices]
        wall_indices = np.where(np.isnan(run_left_utility))
        run_left_utility[wall_indices] = self.__utility[wall_indices]
        return walk_left_utility, run_left_utility

    def right_utility(self):
        last_col = self.__utility[:, self.__col - 1]
        last_col = last_col.reshape(len(last_col), 1)
        last_second_col = self.__utility[:, self.__col - 2]
        last_second_col = last_second_col.reshape(len(last_col), 1)
        walk_right_utility = np.hstack((np.delete(self.__utility, 0, axis=1), last_col))
        run_right_utility = np.hstack((np.delete(self.__utility, 0, axis=1), last_second_col))
        run_right_utility = np.hstack((np.delete(run_right_utility, 0, axis=1), last_col))
        wall_indices = np.where(np.isnan(walk_right_utility))
        run_right_utility[wall_indices] = np.nan
        walk_right_utility[wall_indices] = self.__utility[wall_indices]
        wall_indices = np.where(np.isnan(run_right_utility))
        run_right_utility[wall_indices] = self.__utility[wall_indices]
        return walk_right_utility, run_right_utility

    def value_iteration(self):
        # if self.__min_factor == 0:
        #     return self.__utility
        while True:
            self.iterations += 1
            walk_up_utility, run_up_utility = self.up_utility()
            walk_down_utility, run_down_utility = self.down_utility()
            walk_left_utility, run_left_utility = self.left_utility()
            walk_right_utility, run_right_utility = self.right_utility()

            # walk_up = np.float128(self.__walk_probability * walk_up_utility + \
            #           ((1 - self.__walk_probability) / 2) * walk_left_utility + \
            #           ((1 - self.__walk_probability) / 2) * walk_right_utility)
            # walk_down = np.float128(self.__walk_probability * walk_down_utility + \
            #             ((1 - self.__walk_probability) / 2) * walk_left_utility + \
            #             ((1 - self.__walk_probability) / 2) * walk_right_utility)
            # walk_left = np.float128(self.__walk_probability * walk_left_utility + \
            #             ((1 - self.__walk_probability) / 2) * walk_up_utility + \
            #             ((1 - self.__walk_probability) / 2) * walk_down_utility)
            # walk_right = np.float128(self.__walk_probability * walk_right_utility + \
            #              ((1 - self.__walk_probability) / 2) * walk_up_utility + \
            #              ((1 - self.__walk_probability) / 2) * walk_down_utility)
            # run_up = np.float128(self.__run_probability * run_up_utility + \
            #          ((1 - self.__run_probability) / 2) * run_left_utility + \
            #          ((1 - self.__run_probability) / 2) * run_right_utility)
            # run_down = np.float128(self.__run_probability * run_down_utility + \
            #            ((1 - self.__run_probability) / 2) * run_left_utility + \
            #            ((1 - self.__run_probability) / 2) * run_right_utility)
            # run_left = np.float128(self.__run_probability * run_left_utility + \
            #            ((1 - self.__run_probability) / 2) * run_up_utility + \
            #            ((1 - self.__run_probability) / 2) * run_down_utility)
            # run_right = np.float128(self.__run_probability * run_right_utility + \
            #             ((1 - self.__run_probability) / 2) * run_up_utility + \
            #             ((1 - self.__run_probability) / 2) * run_down_utility)
            walk_up = self.__walk_probability * walk_up_utility + \
                                  ((1 - self.__walk_probability) / 2) * walk_left_utility + \
                                  ((1 - self.__walk_probability) / 2) * walk_right_utility
            walk_down = self.__walk_probability * walk_down_utility + \
                                    ((1 - self.__walk_probability) / 2) * walk_left_utility + \
                                    ((1 - self.__walk_probability) / 2) * walk_right_utility
            walk_left = self.__walk_probability * walk_left_utility + \
                                    ((1 - self.__walk_probability) / 2) * walk_up_utility + \
                                    ((1 - self.__walk_probability) / 2) * walk_down_utility
            walk_right = self.__walk_probability * walk_right_utility + \
                                     ((1 - self.__walk_probability) / 2) * walk_up_utility + \
                                     ((1 - self.__walk_probability) / 2) * walk_down_utility
            run_up = self.__run_probability * run_up_utility + \
                                 ((1 - self.__run_probability) / 2) * run_left_utility + \
                                 ((1 - self.__run_probability) / 2) * run_right_utility
            run_down = self.__run_probability * run_down_utility + \
                                   ((1 - self.__run_probability) / 2) * run_left_utility + \
                                   ((1 - self.__run_probability) / 2) * run_right_utility
            run_left = self.__run_probability * run_left_utility + \
                                   ((1 - self.__run_probability) / 2) * run_up_utility + \
                                   ((1 - self.__run_probability) / 2) * run_down_utility
            run_right = self.__run_probability * run_right_utility + \
                                    ((1 - self.__run_probability) / 2) * run_up_utility + \
                                    ((1 - self.__run_probability) / 2) * run_down_utility

            walk_action_list = [walk_up, walk_down, walk_left, walk_right]
            run_action_list = [run_up, run_down, run_left, run_right]
            all_actions = None

            for walk_action in walk_action_list:
                walk_action = self.__walk_reward + self.__discount_factor * walk_action
                walk_action = walk_action.reshape(1, walk_action.shape[0] * walk_action.shape[1])
                if all_actions is None:
                    all_actions = walk_action
                else:
                    all_actions = np.vstack([all_actions, walk_action])

            for run_action in run_action_list:
                run_action = self.__run_reward + self.__discount_factor * run_action
                run_action = run_action.reshape(1, run_action.shape[0] * run_action.shape[1])
                if all_actions is None:
                    all_actions = walk_action
                else:
                    all_actions = np.vstack([all_actions, run_action])

            max_utility = all_actions.max(axis=0)
            max_utility = max_utility.reshape(self.__row, self.__col)
            max_arg = all_actions.argmax(axis=0)
            max_arg = max_arg.reshape(self.__row, self.__col)
            self.__policy = max_arg
            self.__policy[self.__walls] = -1
            self.__policy[self.__terminals] = -2

            max_utility[self.__terminals] = self.__utility[self.__terminals]
            diff = abs(max_utility - self.__utility)
            diff[self.__walls] = 0
            max_utility[self.__walls] = np.nan
            self.__utility = max_utility
            delta = diff.max()
            if delta <= self.__epsilon * (1 - self.__discount_factor) / self.__discount_factor:
                return self.__utility
        return self.__utility

    def policy_to_string(self):
        result_str = ''
        for row in range(self.__policy.shape[0]):
            row_str = ''
            for col in range(self.__policy.shape[1]):
                action = self.__policy[row, col]
                row_str += self.__action_map.get(action) + ','
            row_str = row_str[:-1] + '\n'
            result_str += row_str
        return result_str

    def write_to_file(self):
        self.__file_io.write_to_file(self.policy_to_string())


vec_solution = VectorSolution()
vec_solution.value_iteration()
vec_solution.write_to_file()
