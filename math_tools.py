""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import math
import matplotlib.pyplot as plt
import numpy as np


SI_CONSTANTS = {'gravity': 9.80665,                                              # in m/s2
                }
CONVERSIONS_FACTORS = {'N-kgf': SI_CONSTANTS['gravity'],                         # Newton to kgf
                       'MPa-kgf/cm2': 100 / SI_CONSTANTS['gravity'],             # MPa to kgf/cm2
                       'kg/m3-kg/cm3': (1 / 1000000),                            # kg/m3 to kg/cm3
                       }


def unit_convert(quantity, conversion, inverse=False):
    """
    Convert float from a physical unit to another.
    Inputs: quantity. Float of value to be converted.
            conversion. String of CONVERSION_FACTORS dict.
                        It determines what conversion to execute.
            inverse. If True, execute inverse conversion.
    Output: Float of converted value.
    """
    if not inverse:                                                              # Execute direct conversion
        return quantity * CONVERSIONS_FACTORS[conversion]
    else:
        return quantity * (1 / CONVERSIONS_FACTORS[conversion])                  # Execute inverse conversion


def array_1d_consecutiveness_check(array):
    """
    Check for consecutiveness of elements of mono-dimensional array.
    Input: Mono-dimensional array.
    Output: Tuple of Boolean, True if consecutiveness is OK, False otherwise,
            and Array of missing positions if they exist.
    """
    array = np.asarray(array)                                                    # Normalize input to numpy array
    array = array.flatten()                                                      # Flatten array
    fail_positions = np.argwhere(np.diff(sorted(array)) > 1) + 2                 # Gather non consecutive values
    return sum(np.diff(sorted(array)) == 1) >= len(array) - 1, fail_positions


def array_extract_unique_sub_arrays(array):
    """
    Returns the input array without repeated sub-arrays.
    Input: Multidimensional array.
    Output: Multidimensional array with only unique sub-arrays.
    """
    types = np.dtype((np.void, array.dtype.itemsize *                            # Deal with data types
                      np.prod(array.shape[1:])))
    b = np.ascontiguousarray(array.reshape(array.shape[0], -1)).view(types)      # Store array efficiently
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
    integral = np.trapz(x, y)                                                    # One variable integration
    plt.plot(x, y, markersize=5, marker='o')                                     # Plot function y=f(x)
    plt.show()
    if verbose:                                                                  # Show numerical value of integral
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
    interpolator = Akima1DInterpolator(independent, dependent)                   # Start interpolator
    new_independent = np.linspace(np.amin(independent),                          # Re-sample independent variable
                                  np.amax(np.asarray(independent)),
                                  10000)
    new_dependent = interpolator(new_independent)                                # Calculate interpolated values
    if plot:                                                                     # Plot original and interpolated curves
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
    solver = nonlinsolve                                                         # Load non linear solver; but if Matrix
    for eq in equations:                                                         # is present, use linear solver
        if isinstance(eq, sp.Matrix):
            solver = linsolve
            break
    solution = solver(equations, *variables)                                     # Solve equations
    solution = {variable: list(solution)[0][pos] for                             # Extract solution expressions
                pos, variable in enumerate(variables)}
    sub = sympy_recursive_substitution                                           # Alias long name function
    if replace_values:                                                           # Replace constants and extract values
        solution = {key: sp.simplify(sub(val, replace_values)) for
                    key, val in solution.items()}
    try:                                                                         # Try to show solution with Latex,
        from IPython.display import display
        sp.init_printing(use_latex=True, forecolor='White')
        display(solution)
    except ImportError:                                                          # if not possible, show with ascii
        print(solution)
    return solution


def primes_generator(amount):
    """
    Generates first n primes.
    Input: int. Amount of primes to be generated.
    Output: list of primes.
    """
    output_list = [2]                                                            # First prime of the list
    number = 3                                                                   # First prime to test with generator
    while len(output_list) < amount:                                             # Generate primes
        primeness = True
        for num in range(2, int(number ** 0.5) + 1):                             # Test primeness
            if number % num == 0:
                primeness = False
                break
        if primeness:                                                            # If prime, append number to list
            output_list.append(number)
        number += 1
    return output_list


def primes_upto(limit):
    """
    Generates all primes up to n.
    Input: int. Max limit of primes to be output.
    Output: list of primes less than or equal to limit."""
    limit = limit + 1                                                            # Move up python limit for generator
    prime = [True] * limit
    for number in range(2, limit):                                               # Generate natural numbers list
        if prime[number]:
            yield number                                                         # Catch prime number
            for c in range(number * number, limit, number):
                prime[c] = False                                                 # Mark composite numbers


def round_up_n(x, base=5):
    """
    Rounds up a float to an integer multiple of base.
    Inputs: x. Float to round up.
            base. Multiple of which to round up to.
    Output: Int of rounded number.
    """
    return int(math.ceil(x / base)) * base


def round_down_n(x, base=5):
    """
    Rounds down a float to an integer multiple of base.
    Inputs: x. Float to round up.
            base. Multiple of which to round up to.
    Output: Int of rounded number.
    """
    return int(math.floor(x / base)) * base


def sympy_recursive_substitution(expression, substitute_dict):
    """
    Recursively substitutes values into sympy expressions.
    They can be numbers or other algebraic expressions.
    Inputs: expression. Sympy algebraic expression.
            substitute_dict. Dict of variable:value pairs.
    Output: Evaluated algebraic expression.
    """
    for _ in range(0, len(substitute_dict) + 1):
        new_expr = expression.subs(substitute_dict)                              # Attempt a symbol eval
        if new_expr == expression:                                               # Check if final expression changes
            return new_expr
        else:                                                                    # Return when no more changes occur
            expression = new_expr
    return


def ishigami_eq(x1, x2, x3):
    """
    The Ishigami function of Ishigami & Homma (1990) is used as an example for uncertainty and sensitivity
    analysis methods, because it exhibits strong non-linearity and no-monotonicity. It also has a peculiar dependence
    on x3, as described by Sobol & Levitan (1999).
    """
    return np.sin(x1) + 7 * np.sin(x2) ** 2 + 0.1 * x3 ** 4 * np.sin(x1)


def white_noise_generator(mean, std, num_samples):
    """
    Generates normalized random values.
    Inputs: mean. Mean of the output array.
            std. Standard deviation of the output array.
    Output: Array of random values.
    """
    return np.random.normal(mean, std, size=num_samples)
