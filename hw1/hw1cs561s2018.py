from sys import maxint

MINI_MAX = 'MINIMAX'
ALPHA_BETA = 'ALPHABETA'
STAR = 'Star'
CIRCLE = 'Circle'


class StateNode:

    def __init__(self):
        self.__neighbours = []
        self.__state = []
        self.__previous_op = None
        self.__final_score = None
        self.__score = None
        self.__alpha = maxint
        self.__beta = -maxint-1
        self.__next_state = None
        for i in range(0, 8):
            self.__state.append([0] * 8)

    def state(self):
        return self.__state

    def set_score(self, score):
        self.__score = score

    def score(self):
        return self.__score

    def set_final_score(self, final_score):
        self.__final_score = final_score

    def final_score(self):
        return self.__final_score

    def clone_state(self, state_node):
        self.__alpha = state_node.alpha()
        self.__beta = state_node.beta()
        self.__score = state_node.score()
        for i in range(8):
            for j in range(8):
                self.__state[i][j] = state_node.state()[i][j]

    def set_op(self, op):
        self.__previous_op = op

    def previous_op(self):
        return self.__previous_op

    def add_neighbour(self, neighbour):
        self.__neighbours.append(neighbour)

    def neighbours(self):
        return self.__neighbours

    def set_value(self, row, col, value):
        self.__state[row][col] = value

    def set_matrix(self, matrix):
        for i in range(8):
            for j in range(8):
                self.__state[i][j] = matrix[i][j]

    def set_alpha(self, alpha):
        self.__alpha = alpha

    def alpha(self):
        return self.__alpha

    def set_beta(self, beta):
        self.__beta = beta

    def beta(self):
        return self.__beta

    def set_next_state(self, next_state):
        self.__next_state = next_state

    def next_state(self):
        return self.__next_state

    def print_state(self):
        for row in self.__state:
            for v in row:
                indent = ' '
                if v != 0:
                    indent = ''
                print v, indent,
            print ''


class NodeOperation:

    inverted_map = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

    def __init__(self, start_position, end_position):
        self.__start_row = start_position[0]
        self.__start_col = start_position[1]
        self.__end_row = end_position[0]
        self.__end_col = end_position[1]

    def get_string(self):
        s = str(self.inverted_map[self.__start_row]) + str(self.__start_col+1)
        e = str(self.inverted_map[self.__end_row]) + str(self.__end_col+1)
        return s+'-'+e


class PlayerCell:

    def __init__(self, s):
        self.__player = 0
        self.__num = 0
        if s == 0:
            return
        if len(s) != 2:
            raise ValueError('Cell String is not valid')
        self.__player = s[0]
        self.__num = int(s[1])

    def increase(self):
        self.__num += 1

    def get_string(self):
        return str(self.__player)+str(self.__num)

    def get_player(self):
        return self.__player

    def get_num(self):
        return self.__num


class ScoreBoard:

    def __init__(self, scores):
        self.__circle_score = []
        self.__star_score = []
        self.__circle_score.extend(scores)
        self.__star_score.extend(scores)
        self.__star_score.reverse()

    def get_score(self, player, row):
        if player == 'S':
            return self.__star_score[row]
        else:
            return self.__circle_score[row]


class StateNodeUtils:

    players = {'S': -1, 'C': 1}

    def __init__(self):
        pass

    @staticmethod
    def check_last_line(player, cur_cell, row, col):
        if player == 'S' and row == 0 and cur_cell.get_player() != 'C':
            return [row, col]
        if player == 'C' and row == 7 and cur_cell.get_player() != 'S':
            return [row, col]
        else:
            return False

    @staticmethod
    def check_cell_validation(player, state_node, row, col, count, is_left):
        new_row = StateNodeUtils.players.get(player) + row
        if new_row > 7 or new_row < 0:
            return False
        new_col = col
        if is_left is True:
            new_col -= 1
            if new_col < 0:
                return False
        else:
            new_col += 1
            if new_col > 7:
                return False
        if state_node.state()[new_row][new_col] == 0:
            return [new_row, new_col]
        cur_cell = PlayerCell(state_node.state()[new_row][new_col])
        last_line = StateNodeUtils.check_last_line(player, cur_cell, new_row, new_col)
        if last_line is not False:
            return last_line
        if state_node.state()[new_row][new_col] != 0 and cur_cell.get_player() != player and count > 0:
            return StateNodeUtils.check_cell_validation(player, state_node, new_row, new_col, count - 1, is_left)
        else:
            return False

    @staticmethod
    def check_validation_left(player, state_node, row, col, count):
        return StateNodeUtils.check_cell_validation(player, state_node, row, col, count, True)

    @staticmethod
    def check_validation_right(player, state_node, row, col, count):
        return StateNodeUtils.check_cell_validation(player, state_node, row, col, count, False)

    @staticmethod
    def check_validation(player, state_node, row, col):
        result = [False, False]
        player_cell = PlayerCell(state_node.state()[row][col])
        if player_cell.get_player() != player:
            return result
        result[0] = StateNodeUtils.check_validation_left(player, state_node, row, col, 1)
        result[1] = StateNodeUtils.check_validation_right(player, state_node, row, col, 1)
        if result[0] is not False and result[1] is not False:
            if result[0][0] > result[1][0]:
                temp = result[0]
                result[0] = result[1]
                result[1] = temp
        return result

    @staticmethod
    def generate_new_state(state_node, start_row, start_col, end_row, end_col):
        new_state_node = StateNode()
        new_state_node.clone_state(state_node)
        cell = PlayerCell(new_state_node.state()[end_row][end_col])
        if cell.get_player() == 0:
            new_state_node.state()[end_row][end_col] = new_state_node.state()[start_row][start_col]
        else:  # last line and cell num increase
            cell.increase()
            new_state_node.state()[end_row][end_col] = cell.get_string()
        new_state_node.state()[start_row][start_col] = 0
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            mid_row = start_row+(end_row-start_row)/2
            mid_col = start_col+(end_col-start_col)/2
            new_state_node.state()[mid_row][mid_col] = 0
        if abs(end_row - start_row) > 2 or abs(end_col - start_col) > 2 or abs(end_row - start_row) == 0 and abs(end_col - start_col) == 0:
            raise RuntimeError('invalid step move')
        new_state_node.set_op(NodeOperation((start_row, start_col), (end_row, end_col)).get_string())
        return new_state_node

    @staticmethod
    def expand_single_cell(player, state_node, row, col):
        expanded_neighbours = []
        validations = StateNodeUtils.check_validation(player, state_node, row, col)
        if validations[0] is not False:
            new_row = validations[0][0]
            new_col = validations[0][1]
            new_state = StateNodeUtils.generate_new_state(state_node, row, col, new_row, new_col)
            expanded_neighbours.append(new_state)
        if validations[1] is not False:
            new_row = validations[1][0]
            new_col = validations[1][1]
            new_state = StateNodeUtils.generate_new_state(state_node, row, col, new_row, new_col)
            expanded_neighbours.append(new_state)
        return expanded_neighbours

    @staticmethod
    def generate_neighbours(state_node, player):
        neighbours = []
        for i in range(8):
            for j in range(8):
                if state_node.state()[i][j] != 0 and state_node.state()[i][j][0] == player:
                    neighbours.extend(StateNodeUtils.expand_single_cell(player, state_node, i, j))
        return neighbours

    @staticmethod
    def calculate_score(state_node, player, score_board):
        total_score = 0
        for row in range(8):
            for col in range(8):
                if state_node.state()[row][col] != 0:
                    player_cell = PlayerCell(state_node.state()[row][col])
                    if player_cell.get_player() == player:
                        total_score += score_board.get_score(player, row) * player_cell.get_num()
                    else:
                        total_score -= score_board.get_score(player_cell.get_player(), row) * player_cell.get_num()
        return total_score

    @staticmethod
    def is_terminate(state_node):
        one_player = None
        for row in range(8):
            for col in range(8):
                if state_node.state()[row][col] != 0:
                    player_cell = PlayerCell(state_node.state()[row][col])
                    if one_player is None:
                        one_player = player_cell.get_player()
                    if player_cell.get_player() != one_player:
                        return False
        return True


class Algorithm:

    def __init__(self, init_state, player, score_board, height):
        self.__opponent_map = {'S': 'C', 'C': 'S'}
        self.__init_state = init_state
        if self.__opponent_map.get(player) is None:
            raise ValueError('player ', player, ' not defined')
        self.__player = player
        self.__score_board = score_board
        self.__height = height

    def execute(self, algorithm_type):
        if algorithm_type == MINI_MAX:
            return self.mini_max_solution()
        if algorithm_type == ALPHA_BETA:
            return self.alpha_beta_solution()

    def mini_max_solution(self):
        return self.mini_max(self.__init_state, self.__height, self.__player, 2)

    def last_state_node(self, state):
        score = StateNodeUtils.calculate_score(state, self.__player, self.__score_board)
        state.set_score(score)
        state.set_final_score(score)
        return 1

    def is_terminate(self, state, height):
        return_value = None
        if height == 0 or StateNodeUtils.is_terminate(state):
            return_value = self.last_state_node(state)
        return return_value

    def is_terminate_by_pass(self, state, neighbours, pass_count):
        return_value = None
        if not neighbours and pass_count == 0:  # terminate
            return_value = self.last_state_node(state)
        return return_value

    def pass_this_round(self, state):
        pass_state = StateNode()
        pass_state.clone_state(state)
        pass_state.set_op('pass')
        return pass_state

    def mini_max(self, state, height, player, pass_count):
        num = 1
        is_terminate = self.is_terminate(state, height)
        if is_terminate is not None:
            return is_terminate
        neighbours = StateNodeUtils.generate_neighbours(state, player)
        is_terminate_by_pass = self.is_terminate_by_pass(state, neighbours, pass_count)
        if is_terminate_by_pass is not None:
            return is_terminate_by_pass
        min_max_score = 0
        if not neighbours:  # pass this round
            pass_state = self.pass_this_round(state)
            result = self.mini_max(pass_state, height - 1, self.__opponent_map.get(player), pass_count - 1)
            num += result
            min_max_score = pass_state.final_score()
            state.set_next_state(pass_state)
            state.add_neighbour(pass_state)
        for neighbour in neighbours:
            state.add_neighbour(neighbour)
            result = self.mini_max(neighbour, height - 1, self.__opponent_map.get(player), 2)
            if state.next_state() is None:
                state.set_next_state(neighbour)
                min_max_score = neighbour.final_score()
            if self.__player == player:  # best next move for player
                if min_max_score < neighbour.final_score():
                    min_max_score = neighbour.final_score()
                    state.set_next_state(neighbour)
            else:  # best next move for opponent
                if min_max_score > neighbour.final_score():
                    min_max_score = neighbour.final_score()
                    state.set_next_state(neighbour)
            num += result
        state.set_final_score(min_max_score)
        return num

    def alpha_beta_solution(self):
        return self.alpha_beta(self.__init_state, self.__height, self.__player, 2)

    def alpha_beta(self, state, height, player, pass_count):
        return self.max_value(state, -maxint-1, maxint, player, height, pass_count)

    def max_value(self, state, alpha, beta, player, height, pass_count):
        num = 1
        is_terminate = self.is_terminate(state, height)
        if is_terminate is not None:
            return is_terminate
        v = -maxint-1
        neighbours = StateNodeUtils.generate_neighbours(state, player)
        is_terminate_by_pass = self.is_terminate_by_pass(state, neighbours, pass_count)
        if is_terminate_by_pass is not None:
            return is_terminate_by_pass
        if not neighbours:  # pass this round
            pass_state = self.pass_this_round(state)
            result = self.min_value(pass_state, alpha, beta, self.__opponent_map.get(player), height - 1, pass_count - 1)
            num += result
            state.set_final_score(pass_state.final_score())
            state.set_next_state(pass_state)
            state.add_neighbour(pass_state)
        for neighbour in neighbours:
            state.add_neighbour(neighbour)
            result = self.min_value(neighbour, alpha, beta, self.__opponent_map.get(player), height - 1, 2)
            num += result
            if v < neighbour.final_score():
                v = neighbour.final_score()
                state.set_next_state(neighbour)
            state.set_final_score(v)
            if v >= beta:
                return num
            alpha = max(alpha, v)
        return num

    def min_value(self, state, alpha, beta, player, height, pass_count):
        num = 1
        is_terminate = self.is_terminate(state, height)
        if is_terminate is not None:
            return is_terminate
        v = maxint
        neighbours = StateNodeUtils.generate_neighbours(state, player)
        is_terminate_by_pass = self.is_terminate_by_pass(state, neighbours, pass_count)
        if is_terminate_by_pass is not None:
            return is_terminate_by_pass
        if not neighbours:  # pass this round
            pass_state = self.pass_this_round(state)
            result = self.max_value(pass_state, alpha, beta, self.__opponent_map.get(player), height - 1, pass_count - 1)
            num += result
            state.set_final_score(pass_state.final_score())
            state.set_next_state(pass_state)
            state.add_neighbour(pass_state)
        for neighbour in neighbours:
            state.add_neighbour(neighbour)
            result = self.max_value(neighbour, alpha, beta, self.__opponent_map.get(player), height - 1, 2)
            num += result
            if v > neighbour.final_score():
                v = neighbour.final_score()
                state.set_next_state(neighbour)
            state.set_final_score(v)
            if v <= alpha:
                return num
            beta = min(beta, v)
        return num


class InputInfo:

    player_map = {STAR: 'S', CIRCLE: 'C'}

    def __init__(self):
        self.__player = None
        self.__algorithm = None
        self.__depth = 0
        self.__init_state_matrix = None
        self.__score_board = None

    def set_player(self, player):
        self.__player = self.player_map.get(player)

    def get_player(self):
        return self.__player

    def set_algorithm(self, algorithm_str):
        self.__algorithm = algorithm_str

    def get_algorithm(self):
        return self.__algorithm

    def set_depth(self, depth):
        self.__depth = int(depth)

    def get_depth(self):
        return self.__depth

    def set_init_state_matrix(self, matrix):
        self.__init_state_matrix = matrix

    def get_init_state_matrix(self):
        return self.__init_state_matrix

    def set_score_board(self, score_board):
        self.__score_board = score_board

    def get_score_board(self):
        return self.__score_board


class OutputInfo:

    def __init__(self):
        self.__next_move = None
        self.__myopic_utility = None
        self.__farsighted_utility = None
        self.__number_of_nodes = None

    def set_next_move(self, next_move):
        self.__next_move = next_move

    def get_next_move(self):
        return self.__next_move

    def set_myopic_utility(self, myopic_utility):
        self.__myopic_utility = myopic_utility

    def get_myopic_utility(self):
        return self.__myopic_utility

    def set_farsighted_utility(self, farsighted_utility):
        self.__farsighted_utility = farsighted_utility

    def get_farsighted_utility(self):
        return self.__farsighted_utility

    def set_number_of_nodes(self, num):
        self.__number_of_nodes = num

    def get_number_of_nodes(self):
        return self.__number_of_nodes


class InputOutput:

    def __init__(self):
        self.__file_name = 'input.txt'
        self.__input_info = InputInfo()
        self.__output_info = OutputInfo()

    def read_file(self):
        fo = open(self.__file_name, 'r+')
        line = ' '
        line_num = 1
        matrix = []
        while line:
            line = fo.readline()
            if line_num == 1:
                self.__input_info.set_player(line.rstrip())
            if line_num == 2:
                self.__input_info.set_algorithm(line.rstrip())
            if line_num == 3:
                self.__input_info.set_depth(line.rstrip())
            if 3 < line_num < 12:
                row = []
                for elem in line.rstrip().split(','):
                    if elem == '0':
                        row.append(0)
                    else:
                        row.append(elem)
                matrix.append(row)
            if line_num == 12:
                score_board = ScoreBoard(map(int, line.rstrip().split(',')))
                self.__input_info.set_score_board(score_board)
            line_num += 1
        self.__input_info.set_init_state_matrix(matrix)
        fo.close()
        return self.__input_info

    def get_input_info(self):
        return self.__input_info

    def set_output_info(self, output_info):
        self.__output_info = output_info

    def write_file(self):
        output_file = open('output.txt', 'w+')
        output_file.write(str(self.__output_info.get_next_move())+'\n')
        output_file.write(str(self.__output_info.get_myopic_utility())+'\n')
        output_file.write(str(self.__output_info.get_farsighted_utility())+'\n')
        output_file.write(str(self.__output_info.get_number_of_nodes()))


class Solution:

    def __init__(self):
        self.__input_output = InputOutput()
        self.__input = None
        self.__output = OutputInfo()
        self.__state = None

    def run(self):
        self.read()
        self.run_logic()
        self.write()

    def read(self):
        self.__input = self.__input_output.read_file()

    def write(self):
        self.__input_output.write_file()

    def run_logic(self):
        init_state = StateNode()
        init_state.set_matrix(self.__input.get_init_state_matrix())
        algorithm = Algorithm(init_state, self.__input.get_player(), self.__input.get_score_board(), self.__input.get_depth())
        nodes_num = algorithm.execute(self.__input.get_algorithm())
        try:
            self.__output.set_next_move(init_state.next_state().previous_op())
            self.__output.set_number_of_nodes(nodes_num)
            self.__output.set_farsighted_utility(init_state.final_score())
            myopic_score = StateNodeUtils.calculate_score(init_state.next_state(), self.__input.get_player(), self.__input.get_score_board())
            self.__output.set_myopic_utility(myopic_score)
            self.__input_output.set_output_info(self.__output)
            self.__state = init_state
        except AttributeError:
            self.__output.set_next_move(None)
            self.__output.set_number_of_nodes(1)
            self.__output.set_farsighted_utility(init_state.final_score())
            self.__output.set_myopic_utility(0)
            self.__input_output.set_output_info(self.__output)
            self.__state = init_state


solution = Solution()
solution.run()
