from __future__ import division

import numpy as np


def nearest_value(array, value):
    """
    Return nearest value in the array.
    """

    idx = (np.abs(array-value)).argmin()
    
    return array[idx], idx


def mult(W, z, a):
    """
    Simplified multiplication of a matrix W with the vectors z and a.
    Vector z will have only 1 or 0 active elements, so we can extract
    only that row of a matrix with the index of the active element.
    Attention: works only if z is binary!
    """
    current_node = z.nonzero()[0]

    # make sure 0 or 1 active elements
    assert len(current_node) < 2

    prod = np.zeros(len(z))

    if len(current_node) != 0:
        # if 1 active, it must be 1
        assert z[current_node] == 1.

        # connection weights from the current node to the neighbours
        prod = W[current_node, :]*a[current_node]

    return prod

def step(x, theta):
    """
    Heaviside step function. Returns 1 if x>=theta,
    otherwise 0.

    Input
    -----
        x:      value
        theta:  threshold
    Output
    ------
        ret:    0 or 1
    """
    ret = np.where(x >= theta, 1, 0)

    return ret


def remove_array_duplicates(x):
    """
    Removes duplicate elements in the array of integers `x` while preserving
    the order of the elements.

    Example
    -------
    >>> x = np.array([10, 10, 3, 3, 3, 8, 8, 8, 8])
    >>> print remove_array_duplicates(x)
    array([10,  3,  8])
    """

    unique = []

    for el in x:
        if el not in unique:
            unique.append(el)

    return np.array(unique, dtype=np.int)
