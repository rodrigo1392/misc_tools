""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import re
import string


def letters_list(start_char='A', end_char='Z', capitalize=True):
    """
    Generates a list of alphabetically order english letters.
    It can go beyond Z, with AA, AB,... format
    Inputs: start_char. Character to start from. 
            end_char. Last character on the list. 
            capitalize. Boolean. If True, output are capital letters 
    Output: List of character strings. 
    """
    base_list = [i for i in string.ascii_lowercase]                              # Get list of ascii characters
    for i in base_list:                                                          # Expand list with 'aa', 'ab', etc.
        base_list = base_list + [i + c for c in string.ascii_lowercase]
    output_list = base_list[base_list.index(start_char.lower()):                 # Extract chars of interest
                            base_list.index(end_char.lower()) + 1]
    if capitalize is True:                                                       # Capitalize chars in output list
        output_list = [c.upper() for c in output_list]
    return output_list


def list_of_lists_unique(input_list):
    """
    Return a flat list of unique values on a list that contains lists.
    Input: input_list. List of lists.
    Output: List of unique values found inside input_list
    """
    return list(set([item for sublist in input_list for item in sublist]))


def sort_strings_by_digit(paths_list):
    """
    Returns a by-digits-sorted version of input strings_list. If digits are not present on the strings,
    then returns the original input strings_list without changes.
    Input: strings_list. List of strings to be sorted.
    Output: List of sorted strings.
    """
    try:
        numbers = [str_extract_last_int(i) for i in paths_list]                  # Extract integers
        paths_list = [x for _, x in sorted(zip(numbers, paths_list))]            # Sort input strings_list by integers
    except IndexError:                                                           # Catch no digits error
        print('WARNING: FILES LIST NOT SORTED BY NUMBER')
    return paths_list


def str_check_if_has_numbers(input_string):
    """
    Return boolean True if the input_string has a digit on it, False otherwise.
    Input: input_string: String to be checked.
    Output: Boolean.
    """
    return any(char.isdigit() for char in input_string)


def str_extract_last_int(input_string):
    """
    Extracts last integer present in a given string
    Input: string. To extract integer from.
    Output: integer value.
    """
    return int(re.findall(r'\d+', str(input_string))[-1])


def str_list_2command_line(input_list):
    """
    Transforms a list into a string, to pass it in a command line.
    Input: input_list. List of strings to be joined.
    Output: Command like string to be passed as command option.
    """
    return "['" + "', '".join(input_list) + "']"
