import numpy as np
import numpy.testing as testing


def test_def_parse_wanted_names(regrid_file):
    from model_evaluation.plotting.plotting import parse_wanted_names
    compare = ['ecmwf_height', 'ecmwf_forecast_time', 'ecmwf_cv']
    x = parse_wanted_names(regrid_file, 'ecmwf')
    assert x == compare


def test_read_data_characters(regrid_file):
    from model_evaluation.plotting.plotting import read_data_characters
    t = np.array([[2, 2], [6, 6], [10, 10]])
    h = np.array([[0.01, 0.014], [0.008, 0.014], [0.009, 0.015]])
    data = np.array([[0, 2], [3, 6], [5, 8]])
    x, y, z = read_data_characters(regrid_file, 'ecmwf_cv', 'ecmwf')
    compare = [data, t, h]
    test = [x, y, z]
    for i in range(3):
        testing.assert_array_almost_equal(compare[i], test[i])


def test_reshape_1d2nd():
    from model_evaluation.plotting.plotting import reshape_1d2nd
    oned = np.array([1, 2, 3, 4])
    twod = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
    compare = np.array([[1, 1], [2, 2], [3, 3], [4, 4]])
    x = reshape_1d2nd(oned, twod)
    testing.assert_array_almost_equal(x, compare)
