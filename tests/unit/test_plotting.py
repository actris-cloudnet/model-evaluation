import pytest

MODEL = 'ecmwf'


class VariableInfo:
    def __init__(self):
        self.name = 'Product'


@pytest.mark.parametrize("key", [
    'cf_V', 'cf_A', 'cf_V_adv', 'cf_A_adv'])
def test_get_cf_title(key):
    from model_evaluation.plotting.plotting import _get_cf_title
    var = VariableInfo()
    field_name = key + '_' + MODEL
    value = 'Product, downsampled by volume from ecmwf'
    if 'A' in key:
        value = 'Product, downsampled by area from ecmwf'
    x = _get_cf_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", [
    'cf_V', 'cf_A',  'cf_V_adv', 'cf_A_adv'])
def test_get_cf_title_cycle(key):
    from model_evaluation.plotting.plotting import _get_cf_title
    var = VariableInfo()
    field_name = key + '_' + MODEL + '_001'
    value = 'Product, downsampled by volume from ecmwf cycle 001'
    if 'A' in key:
        value = 'Product, downsampled by area from ecmwf cycle 001'
    x = _get_cf_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key, value", [
    ('iwc', 'Product downsampled from ecmwf'),
    ('iwc_att', 'Product with good attenuation, downsampled from ecmwf'),
    ('iwc_rain', 'Product with rain, downsampled from ecmwf'),
    ('iwc_adv', 'Product downsampled from ecmwf'),
    ('iwc_att_adv', 'Product with good attenuation, downsampled from ecmwf'),
    ('iwc_rain_adv', 'Product with rain, downsampled from ecmwf')])
def test_get_iwc_title(key, value):
    from model_evaluation.plotting.plotting import _get_iwc_title
    var = VariableInfo()
    field_name = key + '_' + MODEL
    x = _get_iwc_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key, value", [
    ('iwc', 'Product downsampled from ecmwf cycle 001'),
    ('iwc_att', 'Product with good attenuation, downsampled from ecmwf cycle 001'),
    ('iwc_rain', 'Product with rain, downsampled from ecmwf cycle 001'),
    ('iwc_adv', 'Product downsampled from ecmwf cycle 001'),
    ('iwc_att_adv', 'Product with good attenuation, downsampled from ecmwf cycle 001'),
    ('iwc_rain_adv', 'Product with rain, downsampled from ecmwf cycle 001')])
def test_get_iwc_title_cycle(key, value):
    from model_evaluation.plotting.plotting import _get_iwc_title
    var = VariableInfo()
    field_name = key + '_' + MODEL + '_001'
    x = _get_iwc_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", ['lwc','lwc_adv'])
def test_get_product_title(key):
    from model_evaluation.plotting.plotting import _get_product_title
    var = VariableInfo()
    field_name = key + '_' + MODEL
    value = 'Product downsampled from ecmwf'
    x = _get_product_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", ['lwc','lwc_adv'])
def test_get_product_title_cycle(key):
    from model_evaluation.plotting.plotting import _get_product_title
    var = VariableInfo()
    field_name = key + '_' + MODEL + '_001'
    value = 'Product downsampled from ecmwf cycle 001'
    x = _get_product_title(field_name, var)
    assert x == value


@pytest.mark.parametrize("key, title", [
    ('lwc', "Product"),
    ('lwc_adv', "Product (Advection time)")])
def test_get_stat_titles(key, title):
    from model_evaluation.plotting.plotting import _get_stat_titles
    field_name = key + '_' + MODEL
    var = VariableInfo()
    x = _get_stat_titles(field_name, key, var)
    assert x == title


@pytest.mark.parametrize("key", [
    'cf_V', 'cf_A',  'cf_V_adv', 'cf_A_adv'])
def test_get_cf_title_stat(key):
    from model_evaluation.plotting.plotting import _get_cf_title_stat
    field_name = key + '_' + MODEL
    var = VariableInfo()
    x = _get_cf_title_stat(field_name, var)
    value = 'Product volume'
    if 'A' in key:
        value = 'Product area'
    assert x == value


@pytest.mark.parametrize("key, value", [
    ('iwc', 'Product'),
    ('iwc_att', 'Product with good attenuation'),
    ('iwc_rain', 'Product with rain')])
def test_get_iwc_title_stat(key, value):
    from model_evaluation.plotting.plotting import _get_iwc_title_stat
    field_name = key + '_' + MODEL
    var = VariableInfo()
    x = _get_iwc_title_stat(field_name, var)
    assert x == value


@pytest.mark.parametrize("key", ['lwc'])
def test_get_product_title_stat(key):
    from model_evaluation.plotting.plotting import _get_product_title_stat
    var = VariableInfo()
    x = _get_product_title_stat(var)
    assert x == 'Product'
