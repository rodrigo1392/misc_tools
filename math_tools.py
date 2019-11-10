""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import math
import matplotlib.pyplot as plt
import numpy as np


SI_PHYSICAL_CONSTANTS = {'gravity': 9.80665}
CONVERSIONS_FACTORS = {'loco': 1}


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


def detailed_1d_num_integral(x, y, verbose=False):
    """
    Calculates the numerical integral value of y(x), between the limits given by the x array domain.
    Plots the function for more comprehension.
    Inputs: x. Array of independent variable values.
            y. Array of dependent variable values.
            verbose. Optional boolean. If True, print the value of the integral.
    Output: Float value of the integral.
    """
    integral = np.trapz(x, y)
    plt.plot(x, y, markersize=5, marker='o')
    plt.show()
    if verbose:
        print('Integral value:', round(integral, 2))
    return integral


def detailed_1d_interpolator(independent, dependent, plot=True):
    """
    Interpolates a 1 variable function, with the Akima algorithm.
    Inputs: independent. Array of independent variable values.
            dependent. Array of dependent variable values.
            plot. If True, presents original vs interpolated curves.
    Output: Tuple of arrays of interpolated independent and dependent values.
    :return:
    """
    from scipy.interpolate import Akima1DInterpolator
    interpolator = Akima1DInterpolator(independent, dependent)
    new_independent = np.linspace(np.amin(independent),
                                  np.amax(np.asarray(independent)),
                                  10000)
    new_dependent = interpolator(new_independent)
    if plot:
        from matplotlib import pyplot as plt
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        ax.plot(independent, dependent, marker='o')
        ax.plot(new_independent, new_dependent)
        plt.show()
    return new_independent, new_dependent


def detailed_equations_system_solver(variables, equations, replace_values=False):
    """
    Solves system of equations using sympy library.
    Inputs: variables. List of independent variables to be solve for.
            equations. List of sympy equation objects.
            replace_values. If not False, substitute variables for given values in dict form.
    Output: dict of solutions for every variable.
    """
    from sympy.solvers.solveset import nonlinsolve, linsolve
    # Use linear solver if Matrix is present in equation system.
    # Use the non linear solver otherwise
    solver = nonlinsolve
    for eq in equations:
        if isinstance(eq, sp.Matrix):
            solver = linsolve
            break
    solution = solver(equations, *variables)
    solution = {variable: list(solution)[0][pos] for pos, variable in enumerate(variables)}
    if replace_values:
        solution = {key: sp.simplify(sympy_recursive_substitution(val, replace_values)) for
                    key, val in solution.items()}
    try:
        from IPython.display import display
        sp.init_printing(use_latex=True, forecolor='White')
        display(solution)
    except ImportError:
        print(solution)
    return solution


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


def sympy_recursive_substitution(expression, substitute_dict):
    """
    Recursively substitutes values into sympy expressions.
    They can be numbers or other algebraic expressions.
    Inputs: expression. Sympy algebraic expression.
            substitute_dict. Dict of variable:value pairs.
    Output: Evaluated algebraic expression.
    """
    for _ in range(0, len(substitute_dict) + 1):
        new_expr = expression.subs(substitute_dict)
        if new_expr == expression:
            return new_expr
        else:
            expression = new_expr
    return


def ishigami_eq(x1, x2, x3):
    """
    The Ishigami function of Ishigami & Homma (1990) is used as an example for uncertainty and sensitivity
    analysis methods, because it exhibits strong non-linearity and no-monotonicity. It also has a peculiar dependence
    on x3, as described by Sobol & Levitan (1999).
    """
    return np.sin(x1) + 7 * np.sin(x2) ** 2 + 0.1 * x3 ** 4 * np.sin(x1)
