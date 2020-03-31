import numpy as np
import numpy.testing as testing
from datetime import date
import pytest
import netCDF4
from model_evaluation.products.model_products import ModelGrid

MODEL = 'ecmwf'
OUTPUT_FILE = '/home/korpinen/Documents/ACTRIS/model_evaluation/test_data_ecmwf.nc'
PRODUCT = 'iwc'


@pytest.fixture(scope='session')
def file_metadata():
    """Some example global metadata to test file."""
    year, month, day = '2019', '05', '23'
    return {
        'year': year, 'month': month, 'day': day,
        'location': 'Kumpula',
        'case_date': date(int(year), int(month), int(day)),
        'altitude_km': 0.5,
    }


@pytest.fixture(scope='session')
def model_file(tmpdir_factory, file_metadata):
    file_name = tmpdir_factory.mktemp("data").join("file.nc")
    root_grp = netCDF4.Dataset(file_name, "w", format="NETCDF4_CLASSIC")
    time = 3
    level = 2
    root_grp.createDimension('time', time)
    root_grp.createDimension('level', level)
    var = root_grp.createVariable('time', 'f8', 'time')
    var[:] = time
    var = root_grp.createVariable('level', 'f8', 'level')
    var[:] = level
    var = root_grp.createVariable('latitude', 'f8')
    var[:] = 1
    var = root_grp.createVariable('longitude', 'f8')
    var[:] = 1
    var = root_grp.createVariable('horizontal_resolution', 'f8')
    var[:] = 9
    var = root_grp.createVariable('height', 'f8', ('time', 'level'))
    var[:] = np.array([[10, 12, 13],
                       [20, 26, 23]])
    var = root_grp.createVariable('forecast_time', 'f8', 'time')
    var[:] = np.array([1, 5, 10])
    var = root_grp.createVariable('cloud_fraction', 'f8', ('time', 'level'))
    var[:] = np.array([[0, 3, 5],
                       [2, 6, 8]])
    var = root_grp.createVariable('qi', 'f8', ('time', 'level'))
    var[:] = np.array([[0.01, 0.02, 0.06],
                       [0.00, 0.03, 0.08]])
    var = root_grp.createVariable('ql', 'f8', ('time', 'level'))
    var[:] = np.array([[0.08, 0.04, 0.01],
                       [0.09, 0.07, 0.02]])
    var = root_grp.createVariable('temperature', 'f8', ('time', 'level'))
    var[:] = np.array([[300, 302, 305],
                       [301, 299, 298]])
    var = root_grp.createVariable('pressure', 'f8', ('time', 'level'))
    var[:] = np.array([[1000, 1010, 1020],
                       [1001, 1003, 1005]])
    root_grp.close()
    return file_name


@pytest.mark.parametrize("cycle, answer", [
    ('test_file_0-11', '_0-11'), ('test_file', '')])
def test_read_cycle_name(cycle, answer, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    x = obj._read_cycle_name(cycle)
    assert x == answer


def test_get_cv(model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj._get_cv()
    assert f"{MODEL}_cv" in obj.data.keys()


def test_get_iwc(model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj._get_cv()
    assert f"{MODEL}_iwc" in obj.data.keys()


def test_get_lwc(model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj._get_cv()
    assert f"{MODEL}_lwc" in obj.data.keys()


@pytest.mark.parametrize("key", [
    'pressure', 'temperature'])
def test_read_config(key, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    var = obj._read_config('p', 'T')
    assert key in var


@pytest.mark.parametrize("key", [
    'pressure', 'temperature'])
def test_set_variables(key, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    var = obj._set_variables(key)
    x = netCDF4.Dataset(model_file).variables[key]
    testing.assert_almost_equal(x, var)


@pytest.mark.parametrize("p, T, q", [
    (1, 2, 3),
    (20, 40, 80),
    (0.3, 0.6, 0.9)])
def test_calc_water_content(p, T, q, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    x = q * p / (287 * T)
    testing.assert_almost_equal(x, obj._calc_water_content(q, p, T))
    assert True


@pytest.mark.parametrize("key", [
    'time', 'level', 'horizontal_resolution', 'latitude', 'longitude'])
def test_add_common_variables_false(key, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj._is_file = False
    obj._add_variables()
    assert key in obj.data.keys()


@pytest.mark.parametrize("key", [
    'time', 'level', 'horizontal_resolution', 'latitude', 'longitude'])
def test_add_common_variables_true(key, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj._is_file = True
    obj._add_variables()
    assert key not in obj.data.keys()


@pytest.mark.parametrize("key", [
    'height', 'forecast_time'])
def test_add_cycle_variables_no_products(key, model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj._is_file = False
    obj._add_variables()
    assert f"{MODEL}_{key}" in obj.data.keys()
