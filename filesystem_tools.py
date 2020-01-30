""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""


# Flexibility for python 2.x
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
# Flexibility for old versions without pandas
try:
    import pandas as pd
except ImportError:
    pass
import numpy as np
import os
import re
import shutil
import sys
from .strings_tools import sort_strings_by_digit


def check_corrupted_videos(root_path, extensions):
    """
    Checks for video files with given extensions, recursively in the root_path
    Inputs: root_path. Path to be investigated.
            extensions. List of file extensions to look for.
    Output: Tuple of amount of good and bad files.
    """
    try:
        import cv2  # https://pypi.python.org/pypi/opencv-python
    except ImportError:
        sys.exit('NO CV2 MODULE FOUND')
    try:
        import tqdm
        progress_bar = True
    except ImportError:
        print('No tqdm module found. Progress bar will not be shown')
        progress_bar = False
        pass

        # Print Python and CV info
    print("Python version:", sys.version)
    print("CV2:   ", cv2.__version__)

    # Gather paths of video files
    files_paths = files_with_extension_lister(root_path, extensions)

    # Prepare list for progress bar
    if progress_bar:
        files_paths = tqdm.tqdm(files_paths)

    # Process files
    good_files_counter = 0
    for filename in files_paths:
        # produce error
        try:
            vid = cv2.VideoCapture(filename)
            if not vid.isOpened():
                print('FILE NOT FOUND:' + filename)
                raise NameError('File not found')
        except cv2.error:
            print('error:' + filename)
            print("cv2.error:")
        except Exception as e:
            print("Exception:", e)
            print('error:' + filename)
        else:
            good_files_counter += 1

    # OUTPUT MESSAGES
    print("Good files:", good_files_counter)
    print("Bad files:", len(files_paths) - good_files_counter)
    return good_files_counter, len(files_paths) - good_files_counter


def config_file_extract_input(config_file):
    """
    Extract input data from *.cfg file.
    Input: config_file. Cfg file containing input data in an arbitrary
    number of sections and variables.
    Output: Dict of input variable name: value pairs.
    """
    cfg = configparser.ConfigParser()
    cfg.read(config_file)
    # EXTRACT AND PROCESS INPUT DATA
    input_data = ({k: eval(repr(v)) for k, v in cfg.items(i)}
                  for i in cfg.sections())                                        # Generate output for all sections
    input_data = {k: (None if v is '0' else v)
                  for i in input_data for k, v in i.items()}                      # Merge input data in one dict
    output_data = {}
    for k, v in input_data.items():
        try:
            output_data[k] = eval(v)
        except SyntaxError:
            output_data[k] = v
        except TypeError:
            output_data[k] = v
    return output_data


def dataframe_safe_save(data_frame, output_csv, overwrite_csv=False):
    """
    Saves a pandas dataframe to a csv, avoiding non intentional overwriting.
    Inputs: data_frame. Pandas Dataframe to be saved.
            output_csv. Path of output csv.
            overwrite_csv. Boolean, if True, overwrite output file. Do nothing otherwise.
    """
    # Normalize csv file path
    filename_to_print = output_csv.split('/')[-1].replace('.csv', '')
    if os.path.exists(output_csv):
        print('WARNING: CSV FILE EXISTS')
        if overwrite_csv:
            data_frame.to_csv(output_csv, index=False, mode='w+')
            print(filename_to_print, 'CSV FILE OVERWRITTEN')
        else:
            print(filename_to_print, 'CSV FILE NOT SAVED')
    else:
        data_frame.to_csv(output_csv, index=False, mode='w')
        print(filename_to_print, '*** CSV FILE SAVED ***')
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
    strings_list = files_lister(root_path, True, sub_folders_option)
    file_path = [i for i in strings_list if os.path.basename(i) == searched_file]
    if not file_path:
        print('File not found')
        return False
    return file_path


def file_save_with_old_version(filepath):
    """
    Avoids file overwriting, by saving previous version of filepath with and 'old_' prefix
    Input: filepath. Path of file to be saved.
    """
    # Split directory from file name
    folder_path, file_name = os.path.dirname(filepath), os.path.basename(filepath)
    # Save original file with 'old_' prefix
    base_version_file = folder_path + '/old_' + file_name
    if os.path.exists(base_version_file):
        return base_version_file
    # If not previously saved old file is found, create one for future use
    elif os.path.exists(filepath):
        shutil.copy(filepath, base_version_file)
        return base_version_file
    else:
        print(filepath, 'FILE NOT FOUND IN', folder_path)
        return None


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


def files_with_extension_lister(root_path, extensions, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path that matches the extension.
    Inputs: root_path. Path to be investigated.
            extension. List of strings with the extensions of files to be searched for.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of files with extension.
    """
    if not isinstance(extensions, list) and not isinstance(extensions, tuple):
        extensions = [extensions]
    strings_list = files_lister(root_path, full_name_option, sub_folders_option)
    extensions = ['.' + i.replace('.', '') for i in extensions]  # Normalize extensions.
    files_out = [i for i in strings_list if i.endswith(tuple(extensions))]  # Extract only files with given extension.
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


def folder_create_if_not(folder_path):
    """
    Creates folder if it does not exist.
    Input: folder_path. Path of folder to be verified/created.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(folder_path, 'folder created')
    return


def folder_size(start_path='.'):
    """
    Calculates the size of a given folder.
    Input: start_path. Top level folder of interest. If none provided,
    starts on current interpreter chdir.
    Output: Size of folder in MB.
    """
    total_size = 0
    for dir_path, dir_names, file_names in os.walk(start_path):
        for f in file_names:
            fp = os.path.join(dir_path, f)
            total_size += os.path.getsize(fp)
    return total_size/(1024*1024)  # Size in MB


def folder_walk_level(root_path, level=1):
    """
    Returns a generator to be used in a recursively os file walking. It limits the level of sub_folders
    available for the walker algorithm.
    Inputs: root_path. Absolute path of top level folder of interest.
            level. Int, accounts for sub_folders levels.
    Output: Generator.
    """
    root_path = root_path.rstrip(os.path.sep)
    assert os.path.isdir(root_path)
    num_sep = root_path.count(os.path.sep)
    for root, dirs, files in os.walk(root_path):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def peer_strong_motion_2csv(csv_file_path):
    """
    Accommodates typical Strong motion record from PEER, that comes in a plane text file
    with data disposed in horizontal consecutive arrays.
    This function serializes all horizontal data in one single column and returns the
    new data frame in a csv file.
    Input: csv_file_path. Path of the csv file containing strong motion record.
    Output: corrected version of the input file.
    """
    df = pd.read_csv(csv_file_path, header=None)
    df_trans = df.transpose()
    df_out = pd.DataFrame()
    df_out['loco'] = np.array([0])

    column = []
    for i in df_trans:
        column.append(df_trans[i])

    combined = pd.concat(column, ignore_index=True)
    df_out = pd.DataFrame()
    df_out['A'] = combined
    df_out.to_csv(csv_file_path.replace('.csv', '') + '_corrected.csv', index=False)
    return
