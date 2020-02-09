""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import numpy as np


def plot_auto_ticks(input_axes, ticks_amount=4, decimals_n=2, option_identical_axes=False):
    """
    Calculates ticks positions for matplotlib 2D plots.
    Inputs: input_axes. Axes to calculate the ticks for.
            ticks_amount. Int amount of ticks for the axes.
            decimals_n. Int amount of decimals to be printed.
            option_identical_axes. Boolean, if True, ticks for both axes will be identical.
    Output: Tuple of ticks for x and y axes respectively.
    """
    x_min, x_max, y_min, y_max = input_axes()                                    # Extract axes limits
    x_min = round(x_min, decimals_n)                                             # Round limit values
    x_max = round(x_max, decimals_n)
    y_min = round(y_min, decimals_n)
    y_max = round(y_max, decimals_n)
    x_ticks = np.round(np.linspace(x_min, x_max, ticks_amount), decimals_n)      # Generate ticks positions
    y_ticks = np.round(np.linspace(y_min, y_max, ticks_amount), decimals_n)
    if option_identical_axes:                                                    # Use same ticks for both axes
        y_ticks = x_ticks
    return x_ticks, y_ticks


def golden_fig_size(width, fraction=1):
    """
    Set aesthetic figure dimensions to avoid scaling in Latex.
    Inputs: width. Float of width in pts.
            fraction. Float of factor modifier of width.
    Output: Tuple of figure dimensions in inches.
    """
    fig_width_pt = width * fraction                                              # Set width of figure
    inches_per_pt = 1 / 72.27                                                    # Convert from pt to inches
    golden_ratio = (5**.5 - 1) / 2                                               # Calculate golden ratio
    fig_width_in = fig_width_pt * inches_per_pt                                  # Calculate figure width in inches
    fig_height_in = fig_width_in * golden_ratio                                  # Calculate figure height in inches
    return fig_width_in, fig_height_in
