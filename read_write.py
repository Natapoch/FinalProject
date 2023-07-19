def write_parameters(filename, criteria_num, parameters_dict):
    information_index = -1
    information_data = ''
    new_information_data = ''
    flag_criteria = False
    no_information_flag = True
    parameters_file_check(filename)
    with open(filename, 'r') as file_:
        for line in file_.readlines():
            if flag_criteria:
                if line.find(f'K{criteria_num + 1}') != -1:
                    flag_criteria = False
                    new_information_data += line
            elif line.find(f'K{criteria_num}') != -1:
                flag_criteria = True
                no_information_flag = False
                new_information_data += f'K{criteria_num}\n'
                for parameter_name, parameter_value in parameters_dict.items():
                    new_information_data += f'{parameter_name}: {parameter_value}\n'
            else:
                new_information_data += line
    if no_information_flag:
        new_information_data += f'K{criteria_num}\n'
        for parameter_name, parameter_value in parameters_dict.items():
            new_information_data += f'{parameter_name}: {parameter_value}\n'
    with open(filename, 'w') as file_:
        file_.write(new_information_data)

def read_parameters(filename, criteria_num):
    parameters_dict = dict()
    flag_criteria = False
    parameters_file_check(filename)
    with open(filename, 'r') as file_:
        for line in file_.readlines():
            #print('[', line, ']')
            if flag_criteria:
                if line.find(f'K{criteria_num + 1}') != -1:
                    flag_criteria = False
                else:
                    index = line.find(":")
                    parameters_dict[line[:index]] = float(line[index + 2:])
            elif line.find(f'K{criteria_num}') != -1:
                flag_criteria = True
    return parameters_dict

def parameters_file_check(filename):
    try:
        with open(filename, 'r'):
            pass
    except FileNotFoundError:
        with open(filename, 'w'):
            pass
