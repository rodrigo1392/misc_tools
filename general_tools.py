""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero. """
import os
import pickle
import re
import modules.math_tools as math_tools
from time import perf_counter as clock


def files_sorter(files_list):
    """
    Returns a sorted list by digits of input files_list. If digits are not present, returns original input
    file without changes.
    Input: files_list. List of files to be sorted.
    Output: List of sorted files.
    """
    try:
        numbers = [int(re.findall(r'-?\d+\.?\d*', i)[-1].replace('.', '')) for i in files_list]  # Extract integers
        sorted_list = [x for _, x in sorted(zip(numbers, files_list))]  # Sort original file list according to integers
    except IndexError:  # Catch no digits error
        sorted_list = files_list
        print('WARNING: FILES LIST NOT SORTED BY NUMBER')
    return sorted_list


def files_lister(root_path, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path.
    Inputs: root_path. Path to be investigated.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of all existing files.
    """
    root_path = str(root_path)  # Transform Path object into string.
    current_path = os.getcwd()  # Save current directory, because os needs to change to target dir to work fine.
    os.chdir(root_path)
    files_list = []
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            if full_name_option:
                files_list.append(os.path.join(root, file_name))
            else:
                files_list.append(file_name)
        if not sub_folders_option:
            break
    os.chdir(current_path)  # Return to original directory.
    return files_list


def files_with_extension_lister(root_path, extension, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path that matches the extension.
    Inputs: root_path. Path to be investigated.
            extension. String with extension of files to be searched for.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of files with extension.
    """
    files_list = files_lister(root_path, full_name_option, sub_folders_option)
    extension = extension.replace('.', '')  # Delete the . in extension, to normalize it later.
    files_out = [i for i in files_list if i.endswith('.' + extension)]  # Extract only files with given extension.
    sorted_list = files_sorter(files_out)  # Try to sort files by digits. Do nothing otherwise.
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
    files_list = files_lister(root_path, full_name_option, sub_folders_option)
    files_out = [i for i in files_list if input_name in i]  # Extract only files with containing input_name.
    sorted_list = files_sorter(files_out)  # Try to sort files by digits. Do nothing otherwise.
    return sorted_list


def files_in_folder_2txt(root_path, out_file_path, full_name_option=False, sub_folders_option=False):
    """
    Saves all listed files from root_path into a out_file txt.
    Inputs: root_path. Path to be investigated.
            out_file_path. Path of output file.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    """
    if not out_file_path.endswith('.txt'):  # Add txt extension if missing.
        out_file_path = out_file_path + '.txt'
    files_list = files_lister(root_path, full_name_option, sub_folders_option)
    files_list = files_sorter(files_list)  # Try to sort files by digits. Do nothing otherwise.
    with open(out_file_path, 'w+') as file_out:
        for filename in files_list:
            file_out.write(str(filename) + os.linesep)  # Write into output file line by line
    return


def file_finder(root_path, searched_file, sub_folders_option=False):
    """
    Finds a file looking in the root_path. It can return multiple found instances.
    Inputs: root_path. Path to be investigated.
            searched_file. String with file name searched.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders
    Output: Full path(s) of searched file.
    """
    files_list = files_lister(root_path, True, sub_folders_option)
    file_path = [i for i in files_list if os.path.basename(i) == searched_file]
    if not file_path:
        print('File not found')
        return False
    return file_path


def abaqus_parametric_fea_check_files(root_path):
    """
    Checks for availability of sequentially numbered Abaqus output files, using the .log files
    of each job run.
    Input: root_path. Path to investigate.
    Output: Boolean. True if no file is missing and if all .log files statuses are 'COMPLETED'.
            False otherwise.
    """
    root_path = str(root_path)
    files_list = files_with_extension_lister(root_path, 'log', True, False)
    numbers = [int(re.findall(r'-?\d+\.?\d*', i)[-1].replace('.', '')) for i in files_list]
    status_out = True
    check_files, missing_files = math_tools.array_1d_consecutiveness_check(numbers)
    if not check_files:
        print('WARNING: MODELS', missing_files, 'MISSING')
        print('CURRENT NUMBERS: ', numbers)
        status_out = False
    for i in files_list:
        with open(i) as file_read:
            lines_list = file_read.readlines()
            status = lines_list[-1].split(' ')[-1]
        if status != 'COMPLETED\n':
            print('WARNING: JOB ', i, ' NOT COMPLETED')
            status_out = False
    print('Parametric files in ' + root_path + ' in good condition:', status_out)
    return status_out


def files_renumber(files_list, delta):
    """
    Renames all files in files_list, modifing the original name by adding delta to any digit in the files names.
    Input: files_list. List of Full Paths of files to be renamed.
           delta. Int of number to be added.
    """
    for file_name in files_list:
        number = int(re.findall(r'-?\d+\.?\d*', file_name)[-1].replace('.', ''))  # Find numbers in original names.
        new_number = number + delta
        new_file_name = file_name.replace(str(number), str(new_number))
        file_name = file_name.replace('\\\\', '\\')
        os.rename(file_name, new_file_name)  # Rename files.
    return


def str_check_if_has_numbers(input_string):
    """
    Return boolean True if the input_sting has a digit on it, False otherwise.
    Input: input_sting: String to be checked.
    Output: Boolean.
    """
    return any(char.isdigit() for char in input_string)


def str_list_2command_line(input_list):
    """
    Transforms a list into a string, to pass it in a
    command line.
    Input: input_list. List of strings to be joined.
    Output: Command like string to be passed as command option.
    """
    return "['" + "', '".join(input_list) + "']"


def str_from_list(input_list):
    """
    Returns a joined string of input_list.
    Input: input_list. List of strings to be joined.
    Output: String..
    """
    return " ".join(input_list)


def abaqus_process(list_scripts_folder, script_name, options_input, show_process_option):
    """ Runs an script in an Abaqus cae instance.
        list_scripts_folder = Path.
        script_name = str. Script name to be run.
        options_input = dict. Paths and Files names to be passed to the script
        show_process_option = Boolean. If True, shows the CAE window. """
    import subprocess
    with open(PATH_TEMP, 'wb') as fileobject:
        pickle.dump(options_input, fileobject)
    # ******************** Launch abaqus subprocess *******************
    clock_start = clock()
    os.chdir(list_scripts_folder)
    if show_process_option is True:
        proc_state = subprocess.call('abaqus cae -script ' + script_name,
                                     shell=True)
    else:
        proc_state = subprocess.call('abaqus cae noGUI=' + script_name,
                                     shell=True)
    if proc_state == 0:
        print ('Process well runned')
    print('Abaqus time elapsed: ',
          str(round(clock() - clock_start, 2)), ' s')
    # *****************************************************************
    return proc_state


def abaqus_process_2(list_scripts_folder, script_name, options_input, show_process_option):
    PATH_TEMP = options_input['PATH_TEMP']
    import subprocess
    with open(PATH_TEMP, 'wb') as fileobject:
        pickle.dump(options_input, fileobject)
    # ******************** Launch abaqus subprocess *******************
    clock_start = clock()
    os.chdir(list_scripts_folder)
    if show_process_option is True:
        process = subprocess.Popen('abaqus cae -script ' + script_name,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        process.wait()
        out, err = process.communicate()
    else:
        process = subprocess.Popen('abaqus cae noGUI=' + script_name,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        process.wait()
        out, err = process.communicate()
    print(out)
    print(err)
    if process == 0:
        print ('Process well runned')
    print('Abaqus time elapsed: ',
          str(round(clock() - clock_start, 2)), ' s')
    # *****************************************************************
    return process


def abaqus_process3(i_script, show_process_option, args = []):
    """ Runs an script in an Abaqus cae instance.
        list_scripts_folder = Path.
        script_name = str. Script name to be run.
        options_input = dict. Paths and Files names to be passed to the script
        show_process_option = Boolean. If True, shows the CAE window. """
    import subprocess, os
    os.chdir(SCPRITS_FOLDER)
    # ******************** Launch abaqus subprocess *******************
    clock_start = clock()
    args = ' '.join(args)
    if show_process_option is True:
        proc_state = subprocess.call('abaqus cae -script ' + i_script + ' -- ' + args,
                                     shell=True)
        print('abaqus cae -script ' + i_script + ' ' + args)
    else:
        proc_state = subprocess.call('abaqus cae noGUI=' + i_script + ' -- ' + args,
                                     shell=True)
    if proc_state == 0:
        print ('Process well runned')
    print('Abaqus time elapsed: ',
          str(round(clock() - clock_start, 2)), ' s')
    # *****************************************************************
    return proc_state
