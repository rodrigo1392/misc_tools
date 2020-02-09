""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""


# Flexibility for python 2.x
try:
    from pathlib import Path
except ImportError:
    pass
from .strings_tools import list_of_lists_unique
import h5py
import numpy as np
import os
import pandas as pd


def dataframe_safe_save(data_frame, output_csv, overwrite_csv=False):
    """
    Saves a pandas dataframe to a csv, avoiding non intentional overwriting.
    Inputs: data_frame. Pandas Dataframe to be saved.
            output_csv. Path of output csv.
            overwrite_csv. Boolean, if True, overwrite output file.
            Do nothing otherwise.
    """
    output_csv = Path(output_csv).with_suffix('.csv')                            # Normalize csv file path
    if output_csv.exists():                                                      # Check: if csv file exists, and
        print('WARNING: CSV FILE EXISTS')
        if overwrite_csv:                                                        # Overwrite is True
            data_frame.to_csv(output_csv, index=False, mode='w+')                # Save file
            print(Path(output_csv).stem, 'CSV FILE OVERWRITTEN')
        else:
            print(Path(output_csv).stem, 'CSV FILE NOT SAVED')                   # Do not save if overwrite is False
    else:
        data_frame.to_csv(output_csv, index=False, mode='w')                     # If csv does not exist, save it
        print(Path(output_csv).stem, '*** CSV FILE SAVED ***')
    return


def h5db_print_attrs(h5_object):
    """
    Prints main structure of hdf5 file.
    Input: hdf5 opened file to explore.
    """
    def print_attrs(name, _):
        print(name)                                                              # Print filename and attributes
    h5_object.visititems(print_attrs)                                            # Call inner function


def hdf5_swap_groups_and_subgroups(hd, m_keys=None, hd_out=None, verbose=False):
    """
    Creates a new hdf5 file, using first sub group keys as group keys and group keys
    as first sub group keys.
    Inputs: hd. Original hdf5.
            m_keys. List of output hdf5 groups keys.
            hd_out. Path of output file.
            verbose. If True, print output file structure.
    """
    if not hd_out:                                                               # Set default output file path
        hd_out = Path(hd.parent,
                      str(hd.name).replace(hd.stem, str(hd.stem + '_tr')))
    with h5py.File(hd, 'r') as db_file:                                          # Open input hdf5
        if not m_keys:                                                           # Set default groups keys
            m_keys = list_of_lists_unique([v.keys() for v in db_file.values()])
        with h5py.File(hd_out, 'w') as out:                                      # Open output hdf5
            for key in m_keys:                                                   # Iterate trough original subgroups
                out_grp = out.create_group(key)                                  # Swap group names
                for group_n, group in db_file.items():                           # Swap data
                    ds = out_grp.create_dataset(group_n, data=group[key])
                    ds.attrs.update(group.attrs)                                 # Swap datasets attributes
            if verbose:                                                          # Print output file structure
                h5db_print_attrs(out)
    return hd_out


def npz_to_hdf5(npz_files_list, hdf5_path, attributes_dict=None, print_structure=False):
    """
    Saves content of multiple npz files into a hdf5 database file.
    Inputs: npz_files_list. List of Paths of input npz files.
            hdf5_filename. Path of output file.
            attributes_dict. List of groups attributes values.
            print_structure. If True, print structure of output hdf5 file.
    Output: List of output reference values, taken from keys of arrays in npz files.
    """
    if not hdf5_path:
        hdf5_path = Path(npz_files_list[0]).with_suffix('.hdf5')                 # Set default output hdf5 file name
    ref_vars = []
    with h5py.File(hdf5_path, 'w') as output_file:
        for model_pos, npz_path in enumerate(npz_files_list):
            model_no = model_pos + 1                                             # Set npz order as key for hdf5 groups
            grp = output_file.create_group(str(model_no))                        # Create a group for each npz file
            if attributes_dict:                                    # Set values of interest as group attributes
                for k, v in attributes_dict[model_pos]:
                    grp.attrs[k] = v
            arrays = {k: v for k, v in np.load(npz_path).items()}                # Load npz arrays
            ref_vars.extend(arrays.keys())                                       # Set variables refs as datasets keys
            for k, v in arrays.items():                                          # Save npz arrays as datassets
                grp.create_dataset(k, data=v)
    if print_structure:                                                          # Print output file structure
        with h5py.File(hdf5_path, 'r') as f:
            h5db_print_attrs(f)
    return list(set(ref_vars))                                                   # Return list of unique variable refs


def peer_strong_motion_2csv(csv_file_path):
    """
    Accommodates typical Strong motion record from PEER, that comes in a plane text file
    with data disposed in horizontal consecutive arrays.
    This function serializes all horizontal data in one single column and returns the
    new data frame in a csv file.
    Input: csv_file_path. Path of the csv file containing strong motion record.
    Output: corrected version of the input file.
    """
    csv_file_path = Path(csv_file_path).with_suffix('.csv')                      # Normalize input as Path object
    df = pd.read_csv(csv_file_path, header=None)                                 # Read input csv file
    df_trans = df.transpose()                                                    # Transpose data for better handling
    column = []
    for i in df_trans:                                                           # Extract data column wise
        column.append(df_trans[i])
    combined = pd.concat(column, ignore_index=True)                              # Build new dataframe
    df_out = pd.DataFrame()
    df_out['A'] = combined
    df_out.to_csv(Path(str(csv_file_path).                                       # Save corrected csv file
                       replace(csv_file_path.stem,
                               csv_file_path.stem + '_corrected')))
    return
