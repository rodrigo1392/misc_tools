""" Functions to be used by a Python interpreter.
    Developed by Rodrigo Rivero. """
import numpy as np
import pandas as pd
import math, itertools


def round_on_n(x, base=5):
    """

    :param x:    Float to round up
    :param base: Multiple of which to round up to
    :return:     Int of rounded up number
    """
    return int(math.ceil(x / base)) * base


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
            for c in range(number*number, limit, number):
                prime[c] = False  # mark composites


def generate_primes(amount):
    """Generates first n primes.
    Input: int. Amount of primes to be generated.
    Output: list of primes."""
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


def accommodate_strong_motion_data(csv_file_path):
    """
    Function to accommodate typical Strong motion record from PEER, that comes in a csv or similar file
    with the data located in horizontal consecutive arrays. This function serialize all horizontal data in
    one single column and returns the new data frame in another csv file.
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


def empirical_cdf(vector):
    """
    Numerical cumulative density function (CDF)
    Input: vector. Array of empirical data.
    Output: tuple of sorted input data, empirical CDF
    """
    xs = np.sort(vector)
    ys = np.arange(1, len(xs)+1) / float(len(xs))
    return xs, ys


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
    primes = generate_primes(dims_no)
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
            h[j*dims_no + dim] = sum_
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


def array_extract_unique_sub_arrays(array):
    """
    Returns the input array without its repeated sub-arrays.
    Input: Multidimensional array.
    Output: Multidimensional array without repeated sub-arrays.
    """
    types = np.dtype((np.void, array.dtype.itemsize * np.prod(array.shape[1:])))  # Deal with data types
    b = np.ascontiguousarray(array.reshape(array.shape[0], -1)).view(types)  # Store array in efficient way
    return array[np.unique(b, return_index=True)[1]]


def array_1d_consecutiveness_check(array):
    """
    Check for consecutiveness of elements of mono*dimensional array.
    Input: Mono-dimensional array.
    Output: Tuple of Boolean, True if consecutiveness is OK, False otherwise,
            and Array of missing positions if they exist.
    """
    array = np.asarray(array)
    array = array.flatten()
    n = len(array) - 1
    fail_positions = np.argwhere(np.diff(sorted(array)) > 1) + 2
    return sum(np.diff(sorted(array)) == 1) >= n, fail_positions
