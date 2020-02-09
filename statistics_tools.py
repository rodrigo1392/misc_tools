""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

from .math_tools import primes_generator
import math
import numpy as np


def coded2data(c, limits):
    """
    Transforms coded values between -1 and +1 into real scale values.
    Inputs: c. Float of coded value.
            limits. Tuple of the real scale maximum and minimum limits of the parameter.
    Outputs: Float of real value.
    """
    x_max, x_min = max(limits), min(limits)                                      # Extract limits from tuple
    return ((c + 1) * (x_max - x_min) * 0.5) + x_min


def data2coded(x, limits):
    """
    Transforms a given factor value to a relative value between -1 and +1.
    Inputs: x. Float of real value.
            limits. Tuple of the real scale maximum and minimum limits of the parameter.
    Outputs Float of coded value.
    """
    x_max, x_min = max(limits), min(limits)                                      # Extract limits from tuple
    return (2 * (x - x_min) / (x_max - x_min)) - 1


def empirical_cdf(vector):
    """
    Numerical cumulative density function (CDF)
    Input: vector. Array of empirical data.
    Output: tuple of sorted input data, empirical CDF.
    """
    xs = np.sort(vector)                                                         # Sort vector values
    ys = np.arange(1, len(xs) + 1) / float(len(xs))                              # Calculate accumulated percentages
    return xs, ys


def factorial_combination(factors_list):
    """
    Returns all possible combinations of the components of "factors".
    Input: factors. List containing strings to be factorial combined.
    Output: List of factorial combinations.
    """
    if not isinstance(factors_list, list):                                       # Normalize input to list
        factors_list = [factors_list]
    lk = []
    length = len(factors_list)
    for i, element in enumerate(factors_list):                                   # Generate factorial combinator
        if i != length - 1:
            for k in range(i + 1, length):
                lk.append([element, factors_list[k]])
    return lk


def sequence_halton(dims_no, points_no):
    """
    Produces a Halton low discrepancy sequence.
    Inputs: dims_no. Int of number of dimensions (of factors).
            points_no. Int of amounts of sample points to be generated.
    Output: Multidimensional array with generated points between 0 and 1.
    """
    h = np.empty(points_no * dims_no)
    h.fill(np.nan)
    p = np.empty(points_no)
    p.fill(np.nan)
    primes = primes_generator(dims_no)
    log_points = math.log(points_no + 1)
    for dim in range(dims_no):
        prime = primes[dim]
        n = int(math.ceil(log_points / math.log(prime)))
        power = pow
        for t in range(n):
            p[t] = power(prime, -(t + 1))
        for j in range(points_no):
            d = j + 1
            sum_ = math.fmod(d, prime) * p[0]
            for t in range(1, n):
                d = math.floor(d / prime)
                sum_ += math.fmod(d, prime) * p[t]
            h[j * dims_no + dim] = sum_
    return h.reshape(points_no, dims_no)


def sequence_monte_carlo(dims_no, points_no):
    """
    Produces a random sequence of coded values between -1 and 1.
    Inputs: dims_no. Int of number of dimensions (of factors).
            points_no. Int of amounts of sample points to be generated.
    Output: Multidimensional array with generated points between -1 and 1.
    """
    output = np.random.uniform(low=-1, high=1, size=(points_no, dims_no))
    return output
