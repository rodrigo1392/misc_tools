""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import math
import numpy as np


def array_1d_consecutiveness_check(array):
    """
    Check for consecutiveness of elements of mono-dimensional array.
    Input: Mono-dimensional array.
    Output: Tuple of Boolean, True if consecutiveness is OK, False otherwise,
            and Array of missing positions if they exist.
    """
    array = np.asarray(array)
    array = array.flatten()
    n = len(array) - 1
    fail_positions = np.argwhere(np.diff(sorted(array)) > 1) + 2
    return sum(np.diff(sorted(array)) == 1) >= n, fail_positions


def array_extract_unique_sub_arrays(array):
    """
    Returns the input array without its repeated sub-arrays.
    Input: Multidimensional array.
    Output: Multidimensional array with only unique sub-arrays.
    """
    types = np.dtype((np.void, array.dtype.itemsize * np.prod(array.shape[1:])))  # Deal with data types
    b = np.ascontiguousarray(array.reshape(array.shape[0], -1)).view(types)  # Store array in efficient way
    return array[np.unique(b, return_index=True)[1]]


def primes_generator(amount):
    """
    Generates first n primes.
    Input: int. Amount of primes to be generated.
    Output: list of primes.
    """
    output_list = [2]
    number = 3
    while len(output_list) < amount:
        primeness = True
        for num in range(2, int(number ** 0.5) + 1):
            if number % num == 0:
                primeness = False
                break
        if primeness:
            output_list.append(number)
        number += 1
    return output_list


def primes_upto(limit):
    """
    Generates all primes up to n.
    Input: int. Max limit of primes to be output.
    Output: list of primes less than or equal to limit."""
    limit = limit + 1
    prime = [True] * limit
    for number in range(2, limit):
        if prime[number]:
            yield number  # n is a prime
            for c in range(number * number, limit, number):
                prime[c] = False  # mark composites


def round_up_n(x, base=5):
    """
    Rounds up a float to an integer multiple of base.
    Inputs: x. Float to round up.
            base. Multiple of which to round up to.
    Output: Int of rounded number.
    """
    return int(math.ceil(x / base)) * base


def ishigami_eq(x1, x2, x3):
    """
    The Ishigami function of Ishigami & Homma (1990) is used as an example for uncertainty and sensitivity
    analysis methods, because it exhibits strong non-linearity and no-monotonicity. It also has a peculiar dependence
    on x3, as described by Sobol & Levitan (1999).
    """
    return np.sin(x1) + 7 * np.sin(x2) ** 2 + 0.1 * x3 ** 4 * np.sin(x1)
