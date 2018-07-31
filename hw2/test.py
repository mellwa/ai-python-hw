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


class OutputInfo:

    def __init__(self):
        self.__is_valid = None
        self.__groups = []

    def is_valid(self):
        if self.__is_valid == 'Yes':
            return True
        if self.__is_valid == 'No':
            return False
        return None

    def set_yes_no(self, yes_no):
        self.__is_valid = yes_no

    def add_group(self, group):
        self.__groups.append(group)

    def get_groups(self):
        return self.__groups


class FileIO:

    def __init__(self):
        self.__file_name = 'input.txt'
        self.__output_file_name = 'output.txt'
        self.__error_file_name = 'error.txt'
        self.__input_info = InputInfo()
        self.__output_info = OutputInfo()

    def write_to_error_file(self, msg):
        file_obj = open(self.__error_file_name, 'w+')
        file_obj.writelines(msg)
        file_obj.close()

    def read_input(self):
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

    def read_output(self):
        file_obj = open(self.__output_file_name, 'r+')
        line = file_obj.readline()
        section_num = 1
        while line:
            if section_num == 1:
                self.__output_info.set_yes_no(line.rstrip())
            if section_num > 1:
                countries = line.rstrip().split(',')
                if countries is None:
                    raise Exception('no country in the line')
                group = []
                for country in countries:
                    group.append(country)
                self.__output_info.add_group(group)
            section_num += 1
            line = file_obj.readline()
        file_obj.close()

    def get_output(self):
        return self.__output_info


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
        for i in range(self.__input.get_pot_count()):
            country_set.append([])
        str2country = {}
        country_id = 0
        for i in range(len(self.__input.get_pots())):
            pot = self.__input.get_pots()[i]
            for c in pot:
                country = Country()
                country.set_name(c)
                country.set_id(country_id)
                country_id += 1
                country.set_pot(i)
                country_set[i].append(country)
                str2country[c] = country
        for confederation in self.__input.get_confederations():
            country_list = self.__input.get_confederations()[confederation]
            for c in country_list:
                country = str2country[c]
                country.set_confederation(confederation)
        return country_set, str2country


class Hw2Tester:

    def __init__(self):
        self.__FileIO = FileIO()
        self.__FileIO.read_input()
        self.__FileIO.read_output()
        self.__input_info = self.__FileIO.get_input()
        self.__output_info = self.__FileIO.get_output()

        self.__pot_count = self.__input_info.get_pot_count()
        self.__group_count = self.__input_info.get_group_count()
        country_set_creator = CountrySetCreator(self.__input_info)
        country_set, str2country = country_set_creator.create_country_set()
        self.__str2country = str2country
        self.__country_set = country_set

        self.__pot_countdown = []
        for i in range(self.__pot_count):
            self.__pot_countdown.append(1)
        self.__confed_countdown = {}
        self.reset_confed_countdown()
        self.__country_countdown = {}
        for c in str2country.keys():
            self.__country_countdown[c] = 1

    def reset_pot_countdown(self):
        for i in range(self.__pot_count):
            self.__pot_countdown[i] = 1

    def reset_confed_countdown(self):
        for key in self.__input_info.get_confederations().keys():
            self.__confed_countdown[key] = 1
            if key == UEFA:
                self.__confed_countdown[key] += 1

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

    def test(self):
        if self.__output_info.is_valid() is None:
            raise Exception('invalid output')
        if self.__output_info.is_valid() != self.input_validation_checking():
            self.failed('Yes No Failed')
            return
        if self.__output_info.is_valid() is False and self.input_validation_checking() is False:
            self.passed()
            return
        if len(self.__output_info.get_groups()) != self.__group_count:
            self.failed('Invalid group numbers')
            return
        for group in self.__output_info.get_groups():
            self.reset_confed_countdown()
            self.reset_pot_countdown()
            for country in group:
                if country == None_str:
                    continue
                if country not in self.__country_countdown:
                    self.failed('No such a country '+country+' in input file')
                    return
                if self.__country_countdown[country] == 0:
                    self.failed("duplicate country "+country+" occurs")
                    return
                self.__country_countdown[country] -= 1
                country_obj = self.__str2country[country]
                pot = country_obj.get_pot()
                confederation = country_obj.get_confederation()
                if self.__pot_countdown[pot] == 0:
                    self.failed('pot condition contradiction => pot: '+str(pot)+' country: '+country)
                    return
                self.__pot_countdown[pot] -= 1
                if self.__confed_countdown[confederation] == 0:
                    self.failed('confederation condition contradiction => confederation: '+confederation+' country: '+country)
                    return
                self.__confed_countdown[confederation] -= 1
        for key in self.__country_countdown:
            if self.__country_countdown[key] != 0:
                self.failed('country '+key+' is not assigned')
                return
        self.passed()

    def failed(self, str):
        print 'failed'
        self.__FileIO.write_to_error_file(str)

    def passed(self):
        print 'passed'
        return

test = Hw2Tester()
test.test()

