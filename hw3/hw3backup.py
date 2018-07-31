import copy
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
            if section_num == 3: #terminals
                terminal_num = int(line.rstrip())
                for i in range(terminal_num):
                    line = file_obj.readline()
                    terminal = line.rstrip().split(',')
                    if len(terminal) is not 3:
                        raise Exception('wrong terminal position')
                    self.__input_info.add_terminal(terminal)
            if section_num == 4: #probabilities
                probabilities = line.rstrip().split(',')
                if len(probabilities) is not 2:
                    raise Exception('wrong probabilies number')
                self.__input_info.set_walk_probability(probabilities[0])
                self.__input_info.set_run_probability(probabilities[1])
            if section_num == 5: #rewards
                rewards = line.rstrip().split(',')
                if len(rewards) is not 2:
                    raise Exception('wrong rewards number')
                self.__input_info.set_walk_reward(rewards[0])
                self.__input_info.set_run_reward(rewards[1])
            if section_num == 6: #discount factor
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


class Actions:
    WALK = 'Walk'
    RUN = 'Run'

    def __init__(self):
        pass


class Direction:
    UP = 'Up'
    RIGHT = 'Right'
    DOWN = 'Down'
    LEFT = 'Left'

    def __init__(self):
        pass


class Action:
    def __init__(self):
        self.__action = Actions.WALK
        self.__direction = Direction.UP

    def set_action(self, action):
        self.__action = action

    def get_action(self):
        return self.__action

    def set_direction(self, direction):
        self.__direction = direction

    def get_direction(self):
        return self.__direction

    def to_string(self):
        return self.__action + ' ' + self.__direction


class Grid:

    EXIT = 'Exit'

    def __init__(self, row, col):
        self.__total_row = row
        self.__total_col = col
        self.__utility_grid = [[0 for x in range(col)] for y in range(row)]
        self.__policy = [[Action() for x in range(col)] for y in range(row)]
        self.__terminals = []

    def convert_position(self, row, col):
        converted_row = self.__total_row - row
        converted_col = col - 1
        return converted_row, converted_col

    def add_wall(self, wall):
        row, col = self.convert_position(wall[0], wall[1])
        self.__utility_grid[row][col] = None
        self.__policy[row][col] = None

    def add_terminal(self, terminal):
        row, col = self.convert_position(terminal[0], terminal[1])
        self.__utility_grid[row][col] = terminal[2]
        self.__policy[row][col] = self.EXIT
        self.__terminals.append([row, col])

    def is_terminal(self, row, col):
        if self.__policy[row][col] == self.EXIT:
            return True
        return False

    def is_wall(self, row, col):
        if self.__policy[row][col] is None:
            return True
        return False

    def get_utility(self):
        return self.__utility_grid

    def get_policy(self):
        return self.__policy

    def create_grid_with_value(self, value):
        return [[value for x in range(self.__total_col)] for y in range(self.__total_row)]

    def get_terminals(self):
        return self.__terminals


class Solution:

    all_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    all_actions = [Actions.WALK, Actions.RUN]

    def __init__(self):
        self.__file_io = FileIO()
        self.__file_io.read()
        self.__input = self.__file_io.get_input()
        self.__discount_factor = self.__input.get_discount_factor()
        self.__grid = Grid(self.__input.get_grid_row(), self.__input.get_grid_col())
        self.__run_reward = self.__input.get_run_reward()
        self.__walk_reward = self.__input.get_walk_reward()
        self.__run_probability = self.__input.get_run_probability()
        self.__walk_probability = self.__input.get_walk_probability()
        self.__min_terminal_utility = None

        for terminal in self.__input.get_terminals():
            self.__grid.add_terminal(terminal)
            if self.__min_terminal_utility is None:
                self.__min_terminal_utility = terminal[2]
            if terminal[2] < self.__min_terminal_utility:
                self.__min_terminal_utility = terminal[2]

        for wall in self.__input.get_walls():
            self.__grid.add_wall(wall)
        self.__utility = self.__grid.get_utility()
        self.__policy = self.__grid.get_policy()
        self.iterations = 0
        self.__epsilon = 0
        if abs(self.__min_terminal_utility) < 1:
            self.__epsilon = abs(self.__epsilon * self.__min_terminal_utility)

    def get_probability(self, action):
        if action.get_action() is Actions.WALK:
            return self.__walk_probability
        if action.get_action() is Actions.RUN:
            return self.__run_probability

    def get_reward(self, action):
        if action.get_action() is Actions.WALK:
            return self.__walk_reward
        if action.get_action() is Actions.RUN:
            return self.__run_reward

    def alternative_directions(self, direction):
        if direction is Direction.UP:
            return Direction.LEFT, Direction.RIGHT
        if direction is Direction.RIGHT:
            return Direction.UP, Direction.DOWN
        if direction is Direction.DOWN:
            return Direction.RIGHT, Direction.LEFT
        if direction is Direction.LEFT:
            return Direction.DOWN, Direction.UP

    def next_position(self, i, j, action, direction):
        delta, row, col = 0, i, j
        if action is Actions.RUN:
            delta = 2
        if action is Actions.WALK:
            delta = 1
        if direction is Direction.UP:
            row = i - delta
            if row < 0 or self.__grid.is_wall(row, col) or self.__grid.is_wall(i - 1, col):
                row = i
        if direction is Direction.DOWN:
            row = i + delta
            if row >= self.__input.get_grid_row() or self.__grid.is_wall(row, col) or self.__grid.is_wall(i + 1, col):
                row = i
        if direction is Direction.LEFT:
            col = j - delta
            if col < 0 or self.__grid.is_wall(row, col) or self.__grid.is_wall(row, j - 1):
                col = j
        if direction is Direction.RIGHT:
            col = j + delta
            if col >= self.__input.get_grid_col() or self.__grid.is_wall(row, col) or self.__grid.is_wall(row, j + 1):
                col = j
        return row, col

    def calculate_value(self, row, col, action, direction, utility):
        alter_directions = self.alternative_directions(direction)
        next_pos = self.next_position(row, col, action, direction)
        alter_next_pos0 = self.next_position(row, col, action, alter_directions[0])
        alter_next_pos1 = self.next_position(row, col, action, alter_directions[1])
        probability = self.__walk_probability
        if action is Actions.RUN:
            probability = self.__run_probability
        value = probability * utility[next_pos[0]][next_pos[1]] \
            + ((1-probability)/2) * utility[alter_next_pos0[0]][alter_next_pos0[1]] \
            + ((1-probability)/2) * utility[alter_next_pos1[0]][alter_next_pos1[1]]
        return value

    def policy2str(self):
        policy_str = ''
        for row in self.__policy:
            row_str = ''
            for element in row:
                if element is None:
                    row_str += 'None'
                elif element is Grid.EXIT:
                    row_str += Grid.EXIT
                else:
                    row_str += element.to_string()
                row_str += ','
            row_str = row_str[:-1]
            row_str += '\n'
            policy_str += row_str
        return policy_str

    def get_optimal_action_and_value(self, policy_actions, values):
        max_value = values[0]
        for value in values:
            if value > max_value:
                max_value = value
        optimal_actions = []
        for i in range(len(policy_actions)):
            if values[i] == max_value:
                optimal_actions.append(policy_actions[i])
        optimal_action = None
        for simple_action in self.all_actions: # tie breaker
            for direction in self.all_directions:
                for action in optimal_actions:
                    if action.get_action() == simple_action \
                            and action.get_direction() == direction \
                            and optimal_action is None:
                        optimal_action = action
                        return optimal_action, max_value
        return optimal_action, max_value

    def value_iteration(self):
        while True:
            self.iterations += 1
            # current_utility = copy.deepcopy(self.__utility)
            delta = 0
            for i in range(self.__input.get_grid_row()):
                for j in range(self.__input.get_grid_col()):
                    if self.__grid.is_terminal(i, j) or self.__grid.is_wall(i, j):
                        continue
                    policy_actions = []
                    values = []
                    for action in self.all_actions:
                        for direction in self.all_directions:
                            policy_action = Action()
                            policy_action.set_action(action)
                            policy_action.set_direction(direction)
                            utility_value = self.calculate_value(i, j, action, direction, self.__utility)
                            value = self.get_reward(policy_action) + self.__discount_factor * utility_value
                            policy_actions.append(policy_action)
                            values.append(value)
                    optimal_action, max_value = self.get_optimal_action_and_value(policy_actions, values)
                    self.__policy[i][j] = optimal_action
                    previous = self.__utility[i][j]
                    self.__utility[i][j] = max_value
                    if abs(self.__utility[i][j] - previous) > delta:
                        delta = abs(self.__utility[i][j] - previous)
            if delta < self.__epsilon * (1 - self.__discount_factor)/self.__discount_factor:
                return self.__utility

    def get_adjacent_positions(self, position):
        adjacent_positions = []
        # Up
        if position[0] - 1 >= 0 and not self.__grid.is_wall(position[0] - 1, position[1]):
            adjacent_positions.append([position[0] - 1, position[1]])
            if position[0] - 2 >= 0 and not self.__grid.is_wall(position[0] - 2, position[1]):
                adjacent_positions.append([position[0] - 2, position[1]])
        # Down
        if position[0]+1 < self.__input.get_grid_row() and not self.__grid.is_wall(position[0]+1, position[1]):
            adjacent_positions.append([position[0]+1, position[1]])
            if position[0]+2 < self.__input.get_grid_row() and not self.__grid.is_wall(position[0]+2, position[1]):
                adjacent_positions.append([position[0]+2, position[1]])
        #Left
        if position[1]-1 >= 0 and not self.__grid.is_wall(position[0], position[1]-1):
            adjacent_positions.append([position[0], position[1]-1])
            if position[1]-2 >= 0 and not self.__grid.is_wall(position[0], position[1]-2):
                adjacent_positions.append([position[0], position[1]-2])
        #Right
        if position[1]+1 < self.__input.get_grid_col() and not self.__grid.is_wall(position[0], position[1]+1):
            adjacent_positions.append([position[0], position[1]+1])
            if position[1]+2 < self.__input.get_grid_col() and not self.__grid.is_wall(position[0], position[1]+2):
                adjacent_positions.append([position[0], position[1]+2])
        return adjacent_positions

    def improved_value_iteration(self):
        explored_grid = self.__grid.create_grid_with_value(False)
        explore_set = []
        for terminal in self.__grid.get_terminals():
            position = [terminal[0], terminal[1]]
            adjacents = self.get_adjacent_positions(position)
            for adjacent in adjacents:
                if explored_grid[adjacent[0]][adjacent[1]] is False:
                    explore_set.append(adjacent)
                    explored_grid[adjacent[0]][adjacent[1]] = True

        while True:
            self.iterations += 1
            delta = 0
            no_new_position = True
            for explore_position in explore_set:
                i = explore_position[0]
                j = explore_position[1]
                if self.__grid.is_terminal(i, j) or self.__grid.is_wall(i, j):
                    continue
                policy_actions = []
                values = []
                for action in self.all_actions:
                    for direction in self.all_directions:
                        policy_action = Action()
                        policy_action.set_action(action)
                        policy_action.set_direction(direction)
                        utility_value = self.calculate_value(i, j, action, direction, self.__utility)
                        value = self.get_reward(policy_action) + self.__discount_factor * utility_value
                        policy_actions.append(policy_action)
                        values.append(value)
                optimal_action, max_value = self.get_optimal_action_and_value(policy_actions, values)
                self.__policy[i][j] = optimal_action
                previous = self.__utility[i][j]
                self.__utility[i][j] = max_value
                if abs(self.__utility[i][j] - previous) > delta:
                    delta = abs(self.__utility[i][j] - previous)
                # update explore set
                adjacents = self.get_adjacent_positions(explore_position)
                for adjacent in adjacents:
                    if explored_grid[adjacent[0]][adjacent[1]] is False:
                        explore_set.append(adjacent)
                        explored_grid[adjacent[0]][adjacent[1]] = True
                        no_new_position = False

            if delta <= self.__epsilon * (1 - self.__discount_factor)/self.__discount_factor and no_new_position:
                return self.__utility

    def write_to_file(self):
        self.__file_io.write_to_file(self.policy2str())


solution = Solution()
solution.improved_value_iteration()
solution.write_to_file()
