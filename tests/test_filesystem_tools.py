# -*- coding: utf-8 -*-
"""Tests for filesystem_tools module."""

from pathlib import Path
from sample import filesystem_tools as ft


def test_config_extractor():
    """A simple test for config file reader function.

    Check that extracted values correspond to Python objects.
    """

    # Create temporal cfg file.
    example_cfg = Path(Path.cwd(), 'temporal_file.cfg')

    with open(example_cfg, 'w') as cfg_file:
        lines = ["[PARAMETRIC_VARIABLES]",
                 "PARAMETERS_LIST = ['ALPHA_DYN']",
                 "NORMAL_VALUES = [-0.05]",
                 "ANALYSIS_FOLDER = 'C:/abaqus_results/'",
                 "[DATABASE]",
                 "DATABASE_FOLDER = C:/abaqus_results/",
                 "EXTRACTION_ALGORITHM = ''",
                 "[OUTPUT_GATHER]",
                 "GUI = 0"
                 ]
        cfg_file.write('\n'.join(lines))

    # Execute tests.
    config_dict = ft.extract_config_from_cfg(example_cfg)

    int_var = config_dict['gui']
    string1 = config_dict['analysis_folder']
    string2 = config_dict['database_folder']
    empty_str = config_dict['extraction_algorithm']
    float_list = config_dict['normal_values']

    assert isinstance(int_var, int)
    assert isinstance(string1, str)
    assert isinstance(string2, str)
    assert string1 == string2
    assert isinstance(empty_str, str)
    assert isinstance(float_list[0], float)

    # Delete temporal file.
    Path.unlink(example_cfg)
