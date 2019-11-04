""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import os
import re
from strings_tools import sort_strings_by_digit


def file_finder(root_path, searched_file, sub_folders_option=False):
    """
    Finds a file looking in the root_path. It can return multiple found instances.
    Inputs: root_path. Path to be investigated.
            searched_file. String with file name searched.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders
    Output: Full path(s) of searched file.
    """
    strings_list = files_lister(root_path, True, sub_folders_option)
    file_path = [i for i in strings_list if os.path.basename(i) == searched_file]
    if not file_path:
        print('File not found')
        return False
    return file_path


def files_in_folder_2txt(root_path, out_file_path, full_name_option=False, sub_folders_option=False):
    """
    Saves all files found in root_path into a out_file txt.
    Inputs: root_path. Path to be investigated.
            out_file_path. Path of output file.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    """
    if not out_file_path.endswith('.txt'):  # Add txt extension if missing.
        out_file_path = out_file_path + '.txt'
    strings_list = files_lister(root_path, full_name_option, sub_folders_option)
    strings_list = sort_strings_by_digit(strings_list)  # Try to sort files by digits. Do nothing otherwise.
    with open(out_file_path, 'w+') as file_out:
        for filename in strings_list:
            file_out.write(str(filename) + os.linesep)  # Write into output file line by line.
    return


def files_lister(root_path, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path.
    Inputs: root_path. Path to be investigated.
            full_name_option. Boolean, if True, return files with full path, otherwise, just the file names.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of all existing files.
    """
    root_path = str(root_path)  # Transform Path object into string.
    current_path = os.getcwd()  # Save current directory, because os needs to change to target dir to work.
    os.chdir(root_path)  # Change to target folder.
    strings_list = []
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            if full_name_option:
                strings_list.append(os.path.join(root, file_name))
            else:
                strings_list.append(file_name)
        if not sub_folders_option:
            break
    os.chdir(current_path)  # Return to original directory
    return strings_list


def files_renumber(strings_list, delta):
    """
    Renames all files in strings_list, modifying the original name by adding delta to any digit in the files names.
    Input: strings_list. List of Full Paths of files to be renamed.
           delta. Int of number to be added.
    """
    for file_name in strings_list:
        number = int(re.findall(r'-?\d+\.?\d*', file_name)[-1].replace('.', ''))  # Find numbers in original names.
        new_number = number + delta
        new_file_name = file_name.replace(str(number), str(new_number))
        file_name = file_name.replace('\\\\', '\\')
        os.rename(file_name, new_file_name)  # Rename files.
    return


def files_with_extension_lister(root_path, extension, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path that matches the extension.
    Inputs: root_path. Path to be investigated.
            extension. String with the extension of files to be searched for.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of files with extension.
    """
    strings_list = files_lister(root_path, full_name_option, sub_folders_option)
    extension = extension.replace('.', '')  # Delete the . in extension, to normalize it.
    files_out = [i for i in strings_list if i.endswith('.' + extension)]  # Extract only files with given extension.
    sorted_list = sort_strings_by_digit(files_out)  # Try to sort files by digits. Do nothing otherwise.
    return sorted_list


def files_with_name_lister(root_path, input_name, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path that has input_name in it.
    Inputs: root_path. Path to be investigated.
            input_name. String to be looked for in file names.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of files with extension.
    """
    strings_list = files_lister(root_path, full_name_option, sub_folders_option)
    files_out = [i for i in strings_list if input_name in i]  # Extract only files containing input_name on them.
    sorted_list = sort_strings_by_digit(files_out)  # Try to sort files by digits. Do nothing otherwise.
    return sorted_list


