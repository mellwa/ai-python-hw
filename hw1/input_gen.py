import os
import random

STAR = "Star"
CIRCLE = "Circle"
MINIMAX = "MINIMAX"
ALPHABETA = "ALPHABETA"


class OutputInfo:

    def __init__(self):
        self.__player = None
        self.__algorithm = None
        self.__depth = None
        self.__state = None
        self.__score_board = None
        self.__output_file = None

    def set_player(self, player):
        self.__player = player

    def set_algorithm(self, algorithm):
        self.__algorithm = algorithm

    def set_depth(self, depth):
        self.__depth = depth

    def set_state(self, state):
        self.__state = state

    def set_score_board(self, score_board):
        self.__score_board = score_board

    def set_output_file(self, output):
        self.__output_file = output

    def create(self):
        output_file = open(self.__output_file, 'w+')
        output_file.write(str(self.__player)+"\n")
        output_file.write(str(self.__algorithm)+"\n")
        output_file.write(str(self.__depth)+"\n")
        for row in self.__state:
            row_str = ""
            for elem in row:
                row_str += str(elem)
                row_str += ","
            row_str = row_str[:-1]+'\n'
            output_file.write(row_str)
        score_board_row = ""
        for elem in self.__score_board:
            score_board_row += str(elem)
            score_board_row += ","
        score_board_row = score_board_row[:-1]
        output_file.write(score_board_row)


class Generator:

    def __init__(self):
        self.__test_matrix1 = [[0, 'C1', 0,  'C1',  0,  'C1',  0,  'C1'],
                               ['C1',  0,   'C1',  0,  'C1',  0,  'C1',  0],
                               [0,  'S1',   0,  'S1',  0,  'S1',  0,  'S1'],
                               ['S1',  0,   'S1',  0,  'S1',  0,  'S1',  0],
                               [0,  0,   0,  0,  0,  0,  0,  0],
                               [0,  0,   0,  0,  0,  0,  0,  0],
                               [0,  0,   0,  0,  0,  0,  0,  0],
                               [0,  0,   0,  0,  0,  0,  0,  0]]
        self.__dir_name = "input_dir/"
        self.__file_name_prefix = "input"
        self.__file_name_suffix = ".txt"
        self.__score_board = [10, 20, 30, 40, 50, 60, 70, 80]

    def generate(self, player, algorithm, depth, matrix, score_board):
        output = OutputInfo()
        output.set_player(player)
        output.set_algorithm(algorithm)
        output.set_depth(depth)
        output.set_state(matrix)
        output.set_score_board(score_board)
        return output

    def random_pick_elem(self, prob_s, prob_c):
        elem = 0
        if prob_s > 100 or prob_c > 100:
            prob_s = 33
            prob_c = 33
        prob_zero = 100 - prob_s - prob_c
        i = random.randint(1, 100)
        if i < prob_zero+1:
            elem = 0
        elif i < prob_zero+prob_s+1:
            elem = 'S1'
        else:
            elem = 'C1'
        return elem

    def random_matrix(self, prob_s, prob_c):
        state = [[0] * 8 for _ in range(8)]
        s_num, c_num = 0, 0
        for row in range(0, 8):
            start = (row+1) % 2
            for col in xrange(start, 8, 2):
                elem = self.random_pick_elem(prob_s, prob_c)
                if elem == 'S1':
                    s_num += 1
                if elem == 'C1':
                    c_num += 1
                state[row][col] = elem
        if s_num == 0 or c_num == 0:
            return self.random_matrix(prob_s, prob_c)
        return state

    def generate_file_list(self, start_index, file_num):
        if not os.path.exists(self.__dir_name):
            os.mkdir(self.__dir_name)
        cur_index = start_index
        for i in range(file_num):
            prob_s, prob_c = 10, 8
            if cur_index > (start_index + file_num - 1)/ 2:
                prob_s *= 2
                prob_c *= 2
            for player in [STAR, CIRCLE]:
                for algorithm in [MINIMAX, ALPHABETA]:
                    depth = random.randint(3, 8)
                    if algorithm == MINIMAX:
                        depth = random.randint(3, 5)
                    if cur_index > start_index + file_num - 1:
                        break
                    output = self.generate(player, algorithm, depth, self.random_matrix(prob_s, prob_c), self.__score_board)
                    output.set_output_file(self.__dir_name+self.__file_name_prefix+str(cur_index)+self.__file_name_suffix)
                    output.create()
                    cur_index += 1


generator = Generator()
generator.generate_file_list(6, 995)
