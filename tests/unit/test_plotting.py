import numpy as np
import numpy.testing as testing
import pytest

MODEL = 'ecmwf'


class VariableInfo:
    def __init__(self):
        self.name = 'Product'


def test_parse_wanted_names(regrid_file):
    from model_evaluation.plotting.plotting import parse_wanted_names
    compare = ['ecmwf_cf', 'cf_ecmwf']
    x, x_adv = parse_wanted_names(regrid_file, 'cf')
    assert x == compare


def test_parse_wanted_names_adv(regrid_file):
    from model_evaluation.plotting.plotting import parse_wanted_names
    compare = ['ecmwf_cf', 'cf_adv_ecmwf']
    x, x_adv = parse_wanted_names(regrid_file, 'cf')
    assert x_adv == compare


@pytest.mark.parametrize("key", [
    'cf_V', 'cf_A', 'cf_V_adv', 'cf_A_adv'])
def test_get_cf_title(key):
    from model_evaluation.plotting.plotting import get_cf_title
    var = VariableInfo()
    field_name = key + '_' + MODEL
    value = 'Product, downsampled by volume from ecmwf'
    if 'A' in key:
        value = 'Product, downsampled by area from ecmwf'
    x = get_cf_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", [
    'cf_V', 'cf_A',  'cf_V_adv', 'cf_A_adv'])
def test_get_cf_title_cycle(key):
    from model_evaluation.plotting.plotting import get_cf_title
    var = VariableInfo()
    field_name = key + '_' + MODEL + '_001'
    value = 'Product, downsampled by volume from ecmwf cycle 001'
    if 'A' in key:
        value = 'Product, downsampled by area from ecmwf cycle 001'
    x = get_cf_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key, value", [
    ('iwc', 'Product downsampled from ecmwf'),
    ('iwc_att', 'Product with good attenuation, downsampled from ecmwf'),
    ('iwc_rain', 'Product with rain, downsampled from ecmwf'),
    ('iwc_adv', 'Product downsampled from ecmwf'),
    ('iwc_att_adv', 'Product with good attenuation, downsampled from ecmwf'),
    ('iwc_rain_adv', 'Product with rain, downsampled from ecmwf')])
def test_get_iwc_title(key, value):
    from model_evaluation.plotting.plotting import get_iwc_title
    var = VariableInfo()
    field_name = key + '_' + MODEL
    x = get_iwc_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key, value", [
    ('iwc', 'Product downsampled from ecmwf cycle 001'),
    ('iwc_att', 'Product with good attenuation, downsampled from ecmwf cycle 001'),
    ('iwc_rain', 'Product with rain, downsampled from ecmwf cycle 001'),
    ('iwc_adv', 'Product downsampled from ecmwf cycle 001'),
    ('iwc_att_adv', 'Product with good attenuation, downsampled from ecmwf cycle 001'),
    ('iwc_rain_adv', 'Product with rain, downsampled from ecmwf cycle 001')])
def test_get_iwc_title_cycle(key, value):
    from model_evaluation.plotting.plotting import get_iwc_title
    var = VariableInfo()
    field_name = key + '_' + MODEL + '_001'
    x = get_iwc_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", ['lwc','lwc_adv'])
def test_get_product_title(key):
    from model_evaluation.plotting.plotting import get_product_title
    var = VariableInfo()
    field_name = key + '_' + MODEL
    value = 'Product downsampled from ecmwf'
    x = get_product_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", ['lwc','lwc_adv'])
def test_get_product_title_cycle(key):
    from model_evaluation.plotting.plotting import get_product_title
    var = VariableInfo()
    field_name = key + '_' + MODEL + '_001'
    value = 'Product downsampled from ecmwf cycle 001'
    x = get_product_title(field_name, var)
    assert x == value


def test_read_data_characters(regrid_file):
    from model_evaluation.plotting.plotting import read_data_characters
    t = np.array([[2, 2], [6, 6], [10, 10]])
    h = np.array([[0.01, 0.014], [0.008, 0.014], [0.009, 0.015]])
    data = np.array([[0, 2], [3, 6], [5, 8]])
    x, y, z = read_data_characters(regrid_file, 'ecmwf_cf', 'ecmwf')
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

