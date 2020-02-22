# -*- coding: utf-8 -*-
"""Tests for databases_tools module."""


from pathlib import Path

import h5py
import numpy as np

from sample import databases_tools as db


def test_h5_class():
    """A simple test for H5; an enhanced h5py class.

    Check fl_unique_attrs property, restructure_fl method and
    save_npz_in_hdf5 static method.
    """

    # Create temporal hdf5 database.
    example_hdf5 = Path(Path.cwd(), 'temporal_file.hdf5')

    with h5py.File(example_hdf5, 'w') as db_file:
        for model_n in ['1', '2', '3']:
            grp = db_file.create_group('model_' + model_n)
            grp_attrs = {'model_attribute': 'attr_' + model_n}
            grp.attrs.update(grp_attrs)
            for i in ['a', 'b', 'c']:
                dts = grp.create_dataset(i, data=np.asarray([1, 1, 1]))
                dts_attrs = {'data_attribute': 'attr_' + i}
                dts.attrs.update(dts_attrs)

    # Execute tests.
    example_h5 = db.H5(example_hdf5, 'r')
    assert example_h5.fl_unique_attrs == ['data_attribute']
    example_h5.restructure_fl()
    assert example_h5.fl_unique_attrs == ['model_attribute']

    # Close H5 objects and delete temporal files.
    example_h5.close()
    Path.unlink(example_hdf5)

    # Create temporal npz files.
    npz_paths = []
    for model_n in ['1', '2', '3']:
        array_dict = {i: np.asarray([1, 1, 1]) for i in ['a', 'b', 'c']}
        npz_path = Path(Path.cwd(), model_n).with_suffix('.npz')
        np.savez(npz_path, **array_dict)
        npz_paths.append(npz_path)

    # Execute tests
    example_h5 = db.H5.save_npz_in_hdf5(npz_paths)
    assert list(example_h5) == ['1', '2', '3']
    assert list(example_h5['1']) == ['a', 'b', 'c']

    # Close H5 objects and delete temporal files.
    example_h5_path = Path(example_h5.filename)
    example_h5.close()
    Path.unlink(example_h5_path)
    for i in npz_paths:
        Path.unlink(i)
