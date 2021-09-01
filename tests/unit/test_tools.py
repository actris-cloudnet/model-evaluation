import numpy as np
import numpy.ma as ma
import pytest
import numpy.testing as testing
from datetime import datetime, timedelta
from model_evaluation.products.model_products import ModelManager

MODEL = 'ecmwf'
OUTPUT_FILE = '/'
PRODUCT = 'iwc'


def test_model_file_list():
    from model_evaluation.products.tools import check_model_file_list
    name = 'ec'
    models = ['00_ec_1', '00_ec_2', '00_ec_3']
    check_model_file_list(name, models)
    assert True


@pytest.mark.xfail(raises=AttributeError)
def test_model_file_list_fail():
    from model_evaluation.products.tools import check_model_file_list
    name = 'ec'
    models = ['00_ec_1', 'ac_1', '00_ec_2', '00_ec_3']
    check_model_file_list(name, models)


def test_time2datetime():
    from model_evaluation.products.tools import time2datetime
    time_list = [x for x in range(0, 10)]
    d = datetime(2020, 4, 7, 0, 0, 0)
    x = time2datetime(time_list, d)
    compare = [datetime(2020, 4, 7, 0, 0, 0) + timedelta(hours=1 * x) for x in range(0, 10)]
    assert all([a == b for a, b in zip(x, compare)])


def test_rebin_edges():
    from model_evaluation.products.tools import rebin_edges
    data = np.array([1, 3, 6, 10, 15, 21, 28])
    compare = np.array([-1, 2, 4.5, 8, 12.5, 18, 24.5, 35])
    x = rebin_edges(data)
    testing.assert_array_almost_equal(x, compare)


def test_calculate_advection_time_hour(model_file):
    from model_evaluation.products.tools import calculate_advection_time
    obj = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    h = obj.resolution_h
    v = ma.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    s = 1
    compare = h*1000 / v / 60**2
    compare[compare > 1/s] = 1/s
    compare = np.asarray([[timedelta(hours=float(t)) for t in tt] for tt in compare])
    x = calculate_advection_time(h, v, s)
    assert x.all() == compare.all()


def test_calculate_advection_time_10min(model_file):
    from model_evaluation.products.tools import calculate_advection_time
    obj = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    h = obj.resolution_h
    v = ma.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    s = 6
    compare = h*1000 / v / 60**2
    compare[compare > 1/s] = 1/s
    compare = np.asarray([[timedelta(hours=float(t)) for t in tt] for tt in compare])
    x = calculate_advection_time(h, v, s)
    assert x.all() == compare.all()


def test_get_1d_indices():
    from model_evaluation.products.tools import get_1d_indices
    w = (1, 5)
    d = ma.array([0, 1, 2, 3, 4, 5, 6, 7])
    compare = ma.array([0, 1, 1, 1, 1, 0, 0, 0])
    x = get_1d_indices(w, d)
    testing.assert_array_almost_equal(x, compare)


def test_get_1d_indices_mask():
    from model_evaluation.products.tools import get_1d_indices
    w = (1, 5)
    d = ma.array([0, 1, 2, 3, 4, 5, 6, 7])
    m = np.array([0, 0, 1, 0, 0, 1, 0, 1], dtype=bool)
    x = get_1d_indices(w, d, m)
    d[m] = ma.masked
    compare = ma.array([0, 1, ma.masked, 1, 1, ma.masked, 0, ma.masked])
    testing.assert_array_almost_equal(x, compare)


def test_get_adv_indices():
    from model_evaluation.products.tools import get_adv_indices
    mt = 3
    at = 4
    d = ma.array([0, 1, 2, 3, 4, 5, 6, 7])
    compare = ma.array([0, 1, 1, 1, 1, 0, 0, 0], dtype=bool)
    x = get_adv_indices(mt, at, d)
    testing.assert_array_almost_equal(x, compare)


def test_get_adv_indices_mask():
    from model_evaluation.products.tools import get_adv_indices
    mt = 3
    at = 4
    d = ma.array([0, 1, 2, 3, 4, 5, 6, 7])
    m = ma.array([0, 0, 1, 0, 0, 1, 0, 1], dtype=bool)
    x = get_adv_indices(mt, at, d, m)
    d[m] = ma.masked
    compare = ma.array([0, 1, ma.masked, 1, 1, ma.masked, 0, 0])
    testing.assert_array_almost_equal(x, compare)


def test_obs_windows_size():
    from model_evaluation.products.tools import get_obs_window_size
    i = np.array([0, 0, 1, 1, 1, 1, 0], dtype=bool)
    j = np.array([0, 1, 1, 1, 0, 0, 0], dtype=bool)
    x = get_obs_window_size(i, j)
    testing.assert_almost_equal(x, (4, 3))


def test_obs_windows_size_none():
    from model_evaluation.products.tools import get_obs_window_size
    i = np.array([0, 0, 1, 1, 1, 1, 0], dtype=bool)
    j = np.array([0, 0, 0, 0, 0, 0, 0], dtype=bool)
    x = get_obs_window_size(i, j)
    assert x is None

