""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""


# Flexibility for python 2.x
try:
    from pathlib import Path
except ImportError:
    pass
import os
import pandas as pd


def dataframe_safe_save(data_frame, output_csv, overwrite_csv=False):
    """
    Saves a pandas dataframe to a csv, avoiding non intentional overwriting.
    Inputs: data_frame. Pandas Dataframe to be saved.
            output_csv. Path of output csv.
            overwrite_csv. Boolean, if True, overwrite output file. Do nothing otherwise.
    """
    output_csv = Path(output_csv).with_suffix('.csv')               # Normalize csv file path
    if output_csv.exists():
        print('WARNING: CSV FILE EXISTS')
        if overwrite_csv:
            data_frame.to_csv(output_csv, index=False, mode='w+')
            print(Path(output_csv).stem, 'CSV FILE OVERWRITTEN')
        else:
            print(Path(output_csv).stem, 'CSV FILE NOT SAVED')
    else:
        data_frame.to_csv(output_csv, index=False, mode='w')
        print(Path(output_csv).stem, '*** CSV FILE SAVED ***')
    return


def peer_strong_motion_2csv(csv_file_path):
    """
    Accommodates typical Strong motion record from PEER, that comes in a plane text file
    with data disposed in horizontal consecutive arrays.
    This function serializes all horizontal data in one single column and returns the
    new data frame in a csv file.
    Input: csv_file_path. Path of the csv file containing strong motion record.
    Output: corrected version of the input file.
    """
    csv_file_path = Path(csv_file_path).with_suffix('.csv')  # Normalize input as Path object
    df = pd.read_csv(csv_file_path, header=None)             # Read input csv file
    df_trans = df.transpose()                                # Transpose data for better handling
    column = []
    for i in df_trans:
        column.append(df_trans[i])
    combined = pd.concat(column, ignore_index=True)
    df_out = pd.DataFrame()
    df_out['A'] = combined
    df_out.to_csv(Path(str(csv_file_path).replace(csv_file_path.stem, csv_file_path.stem + '_corrected')))
    return
