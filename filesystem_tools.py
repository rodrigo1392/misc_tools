""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    from pathlib import Path
except ImportError:
    pass
import numpy as np
import os
import re
import shutil
import sys
from .strings_tools import sort_strings_by_digit, str_extract_last_int


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
    print("Python version:", sys.version)           # Print Python and CV info
    print("CV2:   ", cv2.__version__)
    files_paths = []                                # Gather paths of video files
    for extension in extensions:
        files_paths.extend(files_with_extension_lister(root_path, extension))
    if progress_bar:                                # Prepare list for progress bar
        files_paths = tqdm.tqdm(files_paths)
    good_files_counter = 0                          # Process files
    for filename in files_paths:
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
    print("Good files:", good_files_counter)        # Output messages
    print("Bad files:", len(files_paths) - good_files_counter)
    return good_files_counter, len(files_paths) - good_files_counter


def config_file_extract_input(config_file):
    """
    Extract input data from *.cfg file.
    Input: config_file. Path of file containing input data in an arbitrary
           number of sections and variables.
    Output: Dict of input variable name: value pairs.
    """
    cfg = configparser.ConfigParser()
    cfg.read(config_file)
    # EXTRACT AND PROCESS INPUT DATA
    input_data = ({k.lower(): eval(repr(v)) for k, v in cfg.items(i)}
                  for i in cfg.sections())                      # Generate output for all sections
    input_data = {k: (None if v is '0' else v)
                  for i in input_data for k, v in i.items()}                      # Merge input data in one dict
    output_data = {}
    for k, v in input_data.items():         # Attempt to convert input strings into Python objects
        try:
            output_data[k] = eval(v)
        except SyntaxError:
            output_data[k] = v
        except TypeError:
            output_data[k] = v
        except:
            output_data[k] = v
    return output_data


def file_finder(root_path, searched_file, sub_folders_option=False):
    """
    Finds a file looking in the root_path. It can return multiple found instances.
    Inputs: root_path. Path to be investigated.
            searched_file. String with file name searched.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders
    Output: Full path(s) of searched file.
    """
    paths_list = files_lister(root_path, True, sub_folders_option)
    file_path = [i for i in paths_list if str(i.name) == searched_file]
    if not file_path:
        print('File not found')
        return False
    return file_path


def file_renumber(file_path, delta):
    """
    Renames a file, modifying its original name, by adding delta to the last digit found in it.
    Input: file_path. Path of file to be renamed.
           delta. Int of number to be added.
    """
    file_path = Path(file_path)                                                       # Normalize input to Path object
    number = str_extract_last_int(file_path)                                          # Find numbers in original names.
    file_path.rename(Path(str(file_path).replace(str(number), str(number + delta))))  # Rename file
    return


def file_save_with_old_version(file_path):
    """
    Avoids file overwriting, by saving previous version of file with and 'old_' prefix.
    Input: file_path. Path of file to be saved.
    """
    file_path = Path(file_path)
    base_version_file = Path(str(file_path).replace(file_path.name, 'old_' + file_path.name))  # Old version file Path
    if base_version_file.exists():                                               # Return old version of file as current
        shutil.copy(str(base_version_file), str(file_path))
        return file_path
    elif Path(file_path).exists():                                               # If not old file is found, create it
        shutil.copy(file_path, base_version_file)
        return file_path
    else:
        print(Path(file_path).name, 'FILE NOT FOUND IN', str(file_path.parent))  # Report if no file was found
        return None


def files_in_folder_2txt(root_path, out_file_path=None, full_name_option=False, sub_folders_option=False):
    """
    Saves all files found in root_path in a txt file.
    Inputs: root_path. Path to be investigated.
            out_file_path. Path of output file.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    """
    if not out_file_path:
        out_file_path = Path(root_path, 'files_list')                           # Assign output file if none provided
    paths_list = files_lister(root_path, full_name_option, sub_folders_option)  # List files in root
    with open(Path(out_file_path).with_suffix('.txt'), 'w+') as file_out:       # Normalize output file suffix and write
        file_out.write('\n'.join(paths_list))
    return out_file_path


def files_lister(root_path, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path.
    Inputs: root_path. Path to be investigated.
            full_name_option. Boolean, if True, return files with full path, otherwise, just the file names.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of all existing files.
    """
    root_path = Path(root_path)                                         # Normalize input to Path object
    if not sub_folders_option:
        paths_list = [f for f in root_path.iterdir() if f.is_file()]    # Get files list
    else:
        paths_list = [f for f in root_path.rglob("*") if f.is_file()]
    if not full_name_option:                                            # Extract only names if necessary
        paths_list = [f.name for f in paths_list]
    try:
        return sort_strings_by_digit(paths_list)                        # Try to sort files by digits
    except IndexError:
        return paths_list


def files_with_extension_lister(root_path, extension, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path with a given extension.
    Inputs: root_path. Path to be investigated.
            extension. String with the file extension to be searched for.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of Path objects.
    """
    paths_list = files_lister(root_path, full_name_option, sub_folders_option)            # List all files in root
    paths_list = [i for i in paths_list if i.suffix == '.' + extension.replace('.', '')]  # Filter by extension
    return paths_list


def files_with_name_lister(root_path, input_string, full_name_option=True, sub_folders_option=True):
    """
    Lists all the files in root_path that contain a given string in its name.
    Inputs: root_path. Path to be investigated.
            input_name. String to be looked for in file names.
            full_name_option. Boolean, if True, return files with full path.
            sub_folder_option. Boolean, if True, do a recursive search in sub-folders.
    Output: List of Path objects.
    """
    paths_list = files_lister(root_path, full_name_option, sub_folders_option)    # List all files in root
    paths_list = [i for i in paths_list if input_string in i.name]                # Filter by substring
    return paths_list


def folder_create_if_not(folder_path):
    """
    Creates folder if it does not exist.
    Input: folder_path. Path of folder to be verified/created.
    """
    folder_path = Path(folder_path)                 # Normalize input to Path object
    try:
        folder_path.mkdir()                         # Attempt to create folder
        print(str(folder_path), 'folder created')
        return folder_path
    except FileExistsError:                         # If it already exists, do nothing
        return folder_path


def folder_size(root_path=None, sub_folders_option=True):
    """
    Calculates the size of a given folder.
    Input: root_path. Root folder of interest. If not given, start on current interpreter dir.
    Output: Size of folder in MB.
    """
    if not root_path:
        root_path = Path.cwd()
    paths_list = files_lister(root_path, True, sub_folders_option)            # List all files in root
    return round(sum(f.stat().st_size for f in paths_list) / (1024*1024), 3)  # Size in MB


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
