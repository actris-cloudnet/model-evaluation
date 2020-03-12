import numpy as np
import numpy.testing as testing
from datetime import date
import pytest
import netCDF4
from model_evaluation.products.generate_modeldata import ModelDataHandler

MODEL = 'ecmwf'
IS_FILE = True


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
    height = 2
    root_grp.createDimension('time', time)
    root_grp.createDimension('height', height)
    var = root_grp.createVariable('time', 'f8', 'time')
    var[:] = time
    var = root_grp.createVariable('height', 'f8', 'height')
    var[:] = height
    var = root_grp.createVariable('cloud_fraction', 'f8', ('time', 'height'))
    var[:] = np.array([[0, 3, 5],
                       [2, 6, 8]])
    var = root_grp.createVariable('qi', 'f8', ('time', 'height'))
    var[:] = np.array([[0.01, 0.02, 0.06],
                       [0.00, 0.03, 0.08]])
    var = root_grp.createVariable('ql', 'f8', ('time', 'height'))
    var[:] = np.array([[0.08, 0.04, 0.01],
                       [0.09, 0.07, 0.02]])
    var = root_grp.createVariable('temperature', 'f8', ('time', 'height'))
    var[:] = np.array([[300, 302, 305],
                       [301, 299, 298]])
    var = root_grp.createVariable('pressure', 'f8', ('time', 'height'))
    var[:] = np.array([[1000, 1010, 1020],
                       [1001, 1003, 1005]])
    root_grp.close()
    return file_name


def test_read_cycle_name():
    assert True


def test_generate_products():
    assert True


def test_get_cv():
    assert True


def test_get_iwc():
    assert True


def test_get_lwc():
    assert True


def test_read_config():
    assert True


def test_set_variables():
    assert True


@pytest.mark.parametrize("p, T, q",[
    (1, 2, 3),
    (20, 40, 80),
    (0.3, 0.6, 0.9)])
def test_calc_water_content(p, T, q, model_file):
    obj = ModelDataHandler(str(model_file), MODEL, IS_FILE)

    assert True


def test_add_variables():
    assert True
