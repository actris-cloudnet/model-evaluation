import numpy as np
import numpy.testing as testing
import pytest


def test_parse_wanted_names(regrid_file):
    from model_evaluation.plotting.plot_tools import parse_wanted_names
    compare = ['ecmwf_cf', 'cf_ecmwf']
    x, x_adv = parse_wanted_names(regrid_file, 'cf')
    assert x == compare


def test_parse_wanted_names_adv(regrid_file):
    from model_evaluation.plotting.plot_tools import parse_wanted_names
    compare = ['ecmwf_cf', 'cf_adv_ecmwf']
    x, x_adv = parse_wanted_names(regrid_file, 'cf')
    assert x_adv == compare


def test_read_data_characters(regrid_file):
    from model_evaluation.plotting.plot_tools import read_data_characters
    t = np.array([[2, 2], [6, 6], [10, 10]])
    h = np.array([[0.01, 0.014], [0.008, 0.014], [0.009, 0.015]])
    data = np.array([[0, 2], [3, 6], [5, 8]])
    x, y, z = read_data_characters(regrid_file, 'ecmwf_cf', 'ecmwf')
    compare = [data, t, h]
    test = [x, y, z]
    for i in range(3):
        testing.assert_array_almost_equal(compare[i], test[i])


def test_reshape_1d2nd():
    from model_evaluation.plotting.plot_tools import reshape_1d2nd
    oned = np.array([1, 2, 3, 4])
    twod = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
    compare = np.array([[1, 1], [2, 2], [3, 3], [4, 4]])
    x = reshape_1d2nd(oned, twod)
    testing.assert_array_almost_equal(x, compare)

