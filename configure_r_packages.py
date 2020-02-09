""" Functions to configure R packages within a Python 3 environment.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""


from rpy2.robjects.packages import importr
utils = importr('utils')
utils.install_packages('rsm')
