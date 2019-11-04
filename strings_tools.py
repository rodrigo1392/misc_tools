""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import re


def str_check_if_has_numbers(input_string):
    """
    Return boolean True if the input_string has a digit on it, False otherwise.
    Input: input_string: String to be checked.
    Output: Boolean.
    """
    return any(char.isdigit() for char in input_string)


def str_list_2command_line(input_list):
    """
    Transforms a list into a string, to pass it in a command line.
    Input: input_list. List of strings to be joined.
    Output: Command like string to be passed as command option.
    """
    return "['" + "', '".join(input_list) + "']"


def sort_strings_by_digit(strings_list):
    """
    Returns a by-digits-sorted version of input strings_list. If digits are not present on the strings,
    then returns the original input strings_list without changes.
    Input: strings_list. List of strings to be sorted.
    Output: List of sorted strings.
    """
    try:
        numbers = [int(re.findall(r'-?\d+\.?\d*', i)[-1].replace('.', '')) for i in strings_list]  # Extract integers
        sorted_list = [x for _, x in sorted(zip(numbers, strings_list))]  # Sort input strings_list by integers
    except IndexError:  # Catch no digits error
        sorted_list = strings_list
        print('WARNING: FILES LIST NOT SORTED BY NUMBER')
    return sorted_list