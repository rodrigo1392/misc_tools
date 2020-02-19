"""Functions to manage pandas and hdf5 databases.

Intended to be used within a Python 3 environment.
Developed by Rodrigo Rivero.
https://github.com/rodrigo1392

"""

# Flexibility for python 2.x
try:
    from pathlib import Path
except ImportError:
    pass

import h5py
import numpy as np
import pandas as pd

from . import strings_tools as st
from . import filesystem_tools as ft


def get_hdf5_first_level_structure(hdf5_path):
    """Extract hdf5 first level groups keys and data-sets attributes.

    Parameters
    ----------
    hdf5_path : Path
        Hdf5 file to be investigated.

    Returns
    -------
    List of str
        Keys of first level groups.
    List of str
        Attributes names of first level data-sets.
    """
    # Open hdf5 file and iterate over first level groups.
    #
    # Retrieve list of groups keys and list of first level data-sets
    # attributes separately.
    with h5py.File(hdf5_path, 'r') as db_file:
        gu = st.get_uniques_in_list_of_lists
        m_keys = [i for i in db_file.keys()]
        m_attrs = gu([list(b.attrs) for v in db_file.values()
                      for b in v.values()])
    return m_keys, m_attrs


def reformat_peer_data_csv(csv_file_path, time_step=0.005):
    """Reformat PEER motion records to column-wise, and save to csv.

    Typically, PEER data is given in a plane text file, with data
    disposed in horizontal consecutive arrays. This function serializes
    it in a single column and returns the new data frame in a csv file.

    Parameters
    ----------
    csv_file_path : Path
        Csv file to load data from.
    time_step : float
        Time step of record. Needs to be set to create time column.

    Returns
    -------
    Path
        Path of corrected cdv file.
    """
    # Normalize input as Path object and read csv file.
    csv_file_path = Path(csv_file_path).with_suffix('.csv')
    df = pd.read_csv(csv_file_path, header=None)

    # Transpose data for handling. Extract it column-wise in new df.
    df_trans = df.transpose()
    column = [df_trans[i] for i in df_trans]
    combined = pd.concat(column, ignore_index=True)

    # Create new data-frame and add time column.
    df_out = pd.DataFrame()
    df_out['T'] = np.arange(0, time_step * (len(combined) - 2), time_step)
    df_out['DATA'] = combined

    # Save corrected csv file in new csv file.
    output_path = ft.modify_filename_in_path(csv_file_path,
                                             added='_corrected', prefix=False)
    df_out.to_csv(output_path, index=False)
    return output_path


def restructure_hdf5_file(hdf5_path, common_sub_groups=None, output_path=None,
                          verbose=False):
    """Reorder hdf5 using common first level subgroups as root groups.

    This function reorganizes hdf5 internal structure, using common
    first level subgroups keys as first level groups keys. This allows
    to regroup outputs from different models under one group for each
    output variable.

    If there are M root groups (corresponding to M models, from M npz
    files) and V output variables, input hdf5 should have M root level
    groups, each of them containing V data sets. This algorithm swaps
    those categories. Therefore, output hdf5  should have V root level
    groups with M data_sets each.

    Attributes are copy from each original group to corresponding
    output data_sets.

    Parameters
    ----------
    hdf5_path : Path
        Hdf5 file to be restructured.
    common_sub_groups : list of str, optional
        Names of first level subgroups keys to use as root groups. If
        not provided, algorithm find and uses all common subgroup keys.
    output_path : Path
        Path of output hdf5 file.
    verbose : bool, optional
        If True, print output hdf5 structure. Default is False.

    Returns
    -------
    output_path : Path
        Path of output hdf5 file.
    """
    # Set default output file path.
    hd = hdf5_path
    if not output_path:
        output_path = Path(hd.parent,
                           str(hd.name).replace(hd.stem, str(hd.stem + '_tr')))

    # Open input hdf5 and set all keys as default groups keys.
    with h5py.File(hd, 'r') as db_file:
        if not common_sub_groups:
            get_unique = st.get_uniques_in_list_of_lists
            common_sub_groups = get_unique([v.keys() for v in db_file.values()])

        # Open output hdf5 file and iterate trough original data-sets,
        # swapping groups names with data, including groups attributes.
        with h5py.File(output_path, 'w') as out:
            for key in common_sub_groups:
                out_grp = out.create_group(key)
                for group_n, group in db_file.items():
                    ds = out_grp.create_dataset(group_n, data=group[key])
                    ds.attrs.update(group.attrs)

            # Print output file structure
            if verbose:
                show_hdf5_structure(out)
    return output_path


def save_dataframe_safely(data_frame, output_csv, overwrite=False):
    """Save pandas dataframe as csv, avoiding accidental overwriting.

    Parameters
    ----------
    data_frame : pandas DataFrame
        To be saved as csv.
    output_csv : Path
        Path of output csv file.
    overwrite : bool, optional
        If True, allow overwrite of output file.

    Returns
    -------
    None
    """
    # Normalize csv file path.
    output_csv = Path(output_csv).with_suffix('.csv')

    # Check output file existence.
    if output_csv.exists():
        print('WARNING: CSV FILE EXISTS')

        # Overwrite if it is allowed.
        if overwrite:
            data_frame.to_csv(output_csv, index=False, mode='w+')
            print(Path(output_csv).stem, 'CSV FILE OVERWRITTEN')

        # Do not save file is overwrite is not allowed.
        else:
            print(Path(output_csv).stem, 'CSV FILE NOT SAVED')

    # If output file does not exist yet, create it.
    else:
        data_frame.to_csv(output_csv, index=False, mode='w')
        print(Path(output_csv).stem, '*** CSV FILE SAVED ***')
    return


def save_npz_in_hdf5(npz_files_list, hdf5_path, attributes_dict=None,
                     verbose=False):
    """Save content of multiple npz numpy arrays to hdf5 file.

    Parameters
    ----------
    npz_files_list : List of Paths
        Npz saved compressed numpy arrays.
    hdf5_path : Path
        Output database hdf5 file.
    attributes_dict : dict of dicts, optional
        Npz identifier : {parameters names : float } pairs. If given,
        add attributes to each npz group. Do nothing otherwise.
    verbose : bool, optional
        If True, print output hdf5 structure. Default is False.

    Returns
    -------
    Path
        Path of output hdf5 file.
    """
    # Set default output hdf5 path.
    if not hdf5_path:
        hdf5_path = Path(npz_files_list[0]).with_suffix('.hdf5')

    # Create output hdf5 file
    #
    # Iterate over npz files list. Create a group  for each npz file,
    # using relative orders as groups keys.
    with h5py.File(hdf5_path, 'w') as output_file:
        for model_pos, npz_path in enumerate(npz_files_list):
            model_no = model_pos + 1
            grp = output_file.create_group(str(model_no))

            # Set values of interest as group attributes.
            if attributes_dict:
                for k, v in attributes_dict[int(model_no)].items():
                    grp.attrs[k] = v

            # Load npz arrays and save them as groups data-sets. Keys
            # will be whatever keys were present in each npz file.
            arrays = {k: v for k, v in np.load(npz_path).items()}
            for k, v in arrays.items():
                grp.create_dataset(k, data=v)

        # Print output file structure
        if verbose:
            show_hdf5_structure(output_file)
    return hdf5_path


def show_hdf5_structure(hdf5_object):
    """Prints main structure of a hdf5 file.

    Parameters
    ----------
    hdf5_object : in-memory loaded hdf5 file
        Must be loaded trough h5py.File or similar.

    Returns
    -------
    None
    """
    # Print filename and attributes by calling inner function.
    def print_attrs(name, _):
        print(name)
    hdf5_object.visititems(print_attrs)
    return
