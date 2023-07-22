# -*- coding: cp1251 -*-
from parser import parse, ending
from parser2 import parse2
from criterion_analyzer import criterion_analyze, all_criteria_analyze
from test_file import test

VERSION = 1.0
EXECUTE_FLAG = True
INPUT_FILE = 'essays.csv'
INPUT_FILE2 = 'essays2.csv'
BEST_PARAMETERS_FILE = 'best_parameters.txt' #����


def not_implemented(*args):
    print("This function isn't implemented")

def exit_func(*args):
    global EXECUTE_FLAG
    EXECUTE_FLAG = False


COMMANDS_LIST = [('parse kritika24', parse),
                 ('parse mogu-pisat', parse2),
                 ('analyze criterion', criterion_analyze),
                 ('analyze all criteria', all_criteria_analyze),
                 ('debug', test),
                 ('exit', exit_func),
                 ]

def read_command():
    return input('Enter required command: ')

def print_commands():
    for num, command in enumerate(COMMANDS_LIST):
        print(f'{num} - {command[0]}')

if __name__ == '__main__':
    print(f'This is final project v.{VERSION}')
    args = [INPUT_FILE, INPUT_FILE2, BEST_PARAMETERS_FILE, ]
    while EXECUTE_FLAG:
        print_commands()
        required_command = read_command()
        try:
            required_command_num = int(required_command)
        except ValueError:
            required_command_num = -1
        for command_num, command in enumerate(COMMANDS_LIST):
            if command_num == required_command_num or command[0] == required_command:
                command[1](*args)


