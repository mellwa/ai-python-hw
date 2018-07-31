AFC = 'AFC'
CAF = 'CAF'
OFC = 'OFC'
CONCACAF = 'CONCACAF'
CONMEBOL = 'CONMEBOL'
UEFA = 'UEFA'
CONFEDERATIONS = [AFC, CAF, OFC, CONCACAF, CONMEBOL, UEFA]
None_str = 'None'
Yes = 'Yes'
No = 'No'


class InputInfo:
    def __init__(self):
        self.__group_count = None
        self.__pot_count = None
        self.pots = []
        self.confederations = {}

    def set_group_count(self, group_count):
        self.__group_count = group_count

    def get_group_count(self):
        return self.__group_count

    def set_pot_count(self, pot_count):
        self.__pot_count = pot_count
        for i in range(pot_count):
            self.pots.append([])

    def get_pot_count(self):
        return self.__pot_count

    def add_country_to_pot(self, country, pot):
        if pot >= len(self.pots):
            raise ValueError('pot number error ', pot, ' ', country)
        self.pots[pot].append(country)

    def add_confederation(self, confederation):
        self.confederations[confederation] = []

    def add_country_to_confederation(self, country, confederation):
        if self.confederations[confederation] is not None:
            self.confederations[confederation].append(country)
        else:
            raise ValueError('confederation ', confederation, ' not exists')

    def get_pots(self):
        return self.pots

    def get_confederations(self):
        return self.confederations


class FileIO:
    def __init__(self):
        self.__file_name = 'input.txt'
        self.__input_info = InputInfo()

    def read(self):
        file_obj = open(self.__file_name, 'r+')
        line = ' '
        section_num = 1
        while line and section_num < 4:
            if section_num == 1:
                line = file_obj.readline()
                self.__input_info.set_group_count(int(line.rstrip()))
            if section_num == 2:
                line = file_obj.readline()
                pot_num = int(line.rstrip())
                self.__input_info.set_pot_count(pot_num)
                for i in range(pot_num):
                    line = file_obj.readline()
                    for country in line.rstrip().split(','):
                        if country != None_str:
                            self.__input_info.add_country_to_pot(country, i)
            if section_num == 3:  # confederation
                for i in range(6):
                    line = file_obj.readline()
                    parts = line.rstrip().split(':')
                    if len(parts) != 2:
                        raise Exception('format error')
                    self.__input_info.add_confederation(parts[0])
                    for country in parts[1].rstrip().split(','):
                        if country != None_str:
                            self.__input_info.add_country_to_confederation(country, parts[0])
            section_num += 1
        file_obj.close()

    def get_input(self):
        return self.__input_info

    def write_to_file(self, output_str):
        output_file = open('output.txt', 'w+')
        output_file.write(output_str)
        output_file.close()


class Country:
    def __init__(self):
        self.__id = None
        self.__name = ''
        self.__confederation = ''
        self.__pot = None

    def set_id(self, given_id):
        self.__id = given_id

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_confederation(self, confederation):
        self.__confederation = confederation

    def get_confederation(self):
        return self.__confederation

    def set_pot(self, pot):
        self.__pot = pot

    def get_pot(self):
        return self.__pot


class CountrySetCreator:
    def __init__(self, input_info):
        self.__input = input_info

    def create_country_set(self):
        country_set = []
        country2id = {}
        id2country = []
        country_id = 0
        try:
            for i in range(self.__input.get_pot_count()):
                country_set.append([])
            for i in range(len(self.__input.get_pots())):
                pot = self.__input.get_pots()[i]
                for c in pot:
                    country = Country()
                    country.set_name(c)
                    country.set_id(country_id)
                    country_id += 1
                    country.set_pot(i)
                    country_set[i].append(country)
                    id2country.append(country)
                    country2id[c] = country.get_id()
            for confederation in self.__input.get_confederations():
                country_list = self.__input.get_confederations()[confederation]
                for c in country_list:
                    country_id = country2id[c]
                    country = id2country[country_id]
                    country.set_confederation(confederation)
        except Exception:
            pass
        return country_set, country2id


class Group:
    def __init__(self, group_id, pot_num):
        self.__id = group_id
        self.__empty_pots = pot_num
        self.__confederation_count = {}
        for confederation in CONFEDERATIONS:
            self.__confederation_count[confederation] = 1
            if confederation == UEFA:
                self.__confederation_count[confederation] = 2
        self.__pots = [None] * pot_num

    def add_country(self, country):
        pot = country.get_pot()
        confederation = country.get_confederation()
        if confederation not in CONFEDERATIONS:
            return False
        if self.__pots[pot] is not None:
            return False
        if self.__confederation_count[confederation] == 0:
            return False
        self.__pots[pot] = country
        self.__empty_pots -= 1
        self.__confederation_count[confederation] -= 1
        return True

    def remove_country(self, country):
        pot = country.get_pot()
        confederation = country.get_confederation()
        if self.__pots[pot] is None:
            return
        self.__pots[pot] = None
        self.__confederation_count[confederation] += 1
        self.__empty_pots += 1

    def to_string(self):
        string = ''
        if self.__empty_pots == len(self.__pots):
            string = None_str
        else:
            for c in self.__pots:
                if c is not None:
                    string += c.get_name()
                    string += ','
            string = string[:-1]
        return string


class GroupBoard:
    def __init__(self, group_num, pot_num):
        self.__groups = []
        for i in range(group_num):
            self.__groups.append(Group(i, pot_num))

    def add_country(self, country, group):
        return self.__groups[group].add_country(country)

    def remove_country(self, country, group):
        self.__groups[group].remove_country(country)

    def to_string(self):
        string = ''
        for i in range(len(self.__groups)):
            string += self.__groups[i].to_string() + '\n'
        string = string[:-1]
        return string


class Distributor:
    def __init__(self):
        self.__FileIO = FileIO()
        self.__FileIO.read()
        self.__input_info = self.__FileIO.get_input()
        self.__pot_count = self.__input_info.get_pot_count()
        self.__group_count = self.__input_info.get_group_count()
        self.__group_board = GroupBoard(self.__input_info.get_group_count(), self.__input_info.get_pot_count())
        country_set_creator = CountrySetCreator(self.__input_info)
        country_set, country2id = country_set_creator.create_country_set()
        self.__country2id = country2id
        self.__country_set = country_set
        self.__unassigned_country = set()
        for country_id in self.__country2id.values():
            self.__unassigned_country.add(country_id)

    def input_validation_checking(self):
        group_count = self.__input_info.get_group_count()
        for pot in self.__input_info.get_pots():
            if len(pot) > group_count:
                return False
        confederations = self.__input_info.get_confederations()
        for confederation in confederations.keys():
            if confederation == UEFA and len(confederations[confederation]) > (group_count * 2):
                return False
            if confederation != UEFA and len(confederations[confederation]) > group_count:
                return False
        return True

    def exceed_remaining_pots(self, group, cur_pot):
        remain_groups = self.__group_count - group - 1
        if len(self.__unassigned_country) > 0 and remain_groups < 0:
            return True
        if len(self.__unassigned_country) == 0 and remain_groups < 0:
            return False
        remain_pots = self.__pot_count - cur_pot
        remain_pots += remain_groups * self.__pot_count
        if remain_pots < len(self.__unassigned_country):
            return True
        return False

    def solution(self):
        result_str = No
        try:
            result_str = self.get_result_str()
        except Exception:
            result_str = No
        self.__FileIO.write_to_file(result_str)

    def get_result_str(self):
        result_output = No
        if self.input_validation_checking() is False:
            return result_output
        result = self.backtracking(0, 0)
        if result is True:
            result_output = Yes + '\n'
            result_output += self.__group_board.to_string()
        return result_output

    def backtracking(self, group, cur_pot):
        if len(self.__unassigned_country) == 0:
            return True
        if self.exceed_remaining_pots(group, cur_pot):
            return False
        result = False
        try:
            for country in self.__country_set[cur_pot]:
                if country.get_id() in self.__unassigned_country and self.__group_board.add_country(country, group) is True:
                    self.__unassigned_country.remove(country.get_id())
                    next_group = group
                    next_pot = cur_pot + 1
                    if next_pot == self.__pot_count:
                        next_pot = 0
                        next_group += 1
                    result = self.backtracking(next_group, next_pot)
                    if result is True:
                        return result
                    self.__unassigned_country.add(country.get_id())
                    self.__group_board.remove_country(country, group)
            if result is False:  # do not set a country at this position
                next_group = group
                next_pot = cur_pot + 1
                if next_pot == self.__pot_count:
                    next_pot = 0
                    next_group += 1
                result = self.backtracking(next_group, next_pot)
        except:
            return False
        return result


distributor = Distributor()
distributor.solution()
