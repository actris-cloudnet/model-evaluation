import numpy as np
import numpy.testing as testing
import pytest
from datetime import time, datetime, timedelta
from model_evaluation.products.generate_grid_product import ObservationManager
from model_evaluation.products.model_products import ModelGrid
from cloudnetpy.products.product_tools import CategorizeBits


MODEL = 'ecmwf'
OUTPUT_FILE = '/home/korpinen/Documents/ACTRIS/model_evaluation/test_data_ecmwf.nc'
PRODUCT = 'iwc'


class CatBits:
    def __init__(self):
        self.category_bits = {'droplet': np.asarray([[1, 0, 1, 1, 1, 1],
                                                     [0, 1, 1, 1, 0, 0]], dtype=bool),
                              'falling': np.asarray([[0, 0, 0, 0, 1, 0],
                                                     [0, 0, 0, 1, 1, 1]], dtype=bool),
                              'cold': np.asarray([[0, 0, 1, 1, 0, 0],
                                                  [0, 1, 1, 1, 0, 1]], dtype=bool),
                              'melting': np.asarray([[1, 0, 1, 0, 0, 0],
                                                     [1, 1, 0, 0, 0, 0]], dtype=bool),
                              'aerosol': np.asarray([[1, 0, 1, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0]], dtype=bool),
                              'insect': np.asarray([[1, 1, 0, 0, 0, 0],
                                                    [0, 0, 1, 0, 0, 0]], dtype=bool)}


def test_regridded_array(model_file, obs_file):
    from model_evaluation.products.generate_grid_product import regrid_array
    m_obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    m_obj.append_data(np.array([[1, 2], [3, 1], [2, 3]]), 'data')
    m_obj.keys['data'] = 'data'
    o_obj = ObservationManager('data', str(obs_file))
    regrid_array(o_obj, m_obj, MODEL, 'data')
    x = m_obj.data['data_obs_ecmwf'][:]
    compare = np.array([[3.5, 6.25], [4.5, 2], [4.5, 4]])
    testing.assert_array_almost_equal(compare, x)


def test_time2datetime():
    from model_evaluation.products.generate_grid_product import time2datetime
    time_list = [x for x in range(0, 10)]
    d = datetime(2020, 4, 7, 0, 0, 0)
    x = time2datetime(time_list, d)
    compare = [datetime(2020, 4, 7, 0, 0, 0) + timedelta(hours=1 * x) for x in range(0, 10)]
    assert all([a == b for a, b in zip(x, compare)])


def test_get_date(obs_file):
    obj = ObservationManager(PRODUCT, str(obs_file))
    date = datetime(2019, 5, 23, 0, 0, 0)
    assert obj._get_date() == date


@pytest.mark.parametrize("key",[
    "iwc", "lwc", "cv"])
def test_generate_product(key, obs_file):
    obj = ObservationManager(key, str(obs_file))
    obj._generate_product()
    assert key in obj.data.keys()


def test_add_height(obs_file):
    obj = ObservationManager(PRODUCT, str(obs_file))
    obj._generate_product()
    assert 'height' in obj.data.keys()


def test_generate_cv(obs_file):
    obj = ObservationManager('cv', str(obs_file))
    compare = obj._generate_cv()
    x = np.array([[0, 1, 0, 0], [0, 0, 0, 1],
                  [1, 0, 0, 0], [0, 0, 0, 1]])
    testing.assert_array_almost_equal(compare, x)


def test_basic_cloud_mask(obs_file):
    cat = CategorizeBits(str(obs_file))
    obj = ObservationManager('cv', str(obs_file))
    compare = obj._classify_basic_mask(cat.category_bits)
    print("testi")
    print(compare)
    x = np.array([[0, 1, 2, 0], [2, 0, 0, 1],
                  [1, 0, 0, 0], [0, 0, 0, 1],
                  [0, 0, 6, 6], [7, 2, 0, 7]])
    testing.assert_array_almost_equal(x, compare)


def test_mask_cloud_bits(obs_file):
    cat = CategorizeBits(str(obs_file))
    obj = ObservationManager('cv', str(obs_file))
    mask = obj._classify_basic_mask(cat.category_bits)
    compare = obj._mask_cloud_bits(mask)
    x = np.array([[0, 1, 0, 0], [0, 0, 0, 1],
                  [1, 0, 0, 0], [0, 0, 0, 1],
                  [0, 0, 0, 0], [0, 0, 0, 0]])
    testing.assert_array_almost_equal(x, compare)


def test_basic_cloud_mask_all_values(obs_file):
    cat = CatBits()
    obj = ObservationManager('cv', str(obs_file))
    compare = obj._classify_basic_mask(cat.category_bits)
    x = np.array([[8, 7, 6, 1, 3, 1],
                  [0, 1, 7, 5, 2, 4]])
    testing.assert_array_almost_equal(x, compare)


def test_mask_cloud_bits_all_values(obs_file):
    cat = CatBits()
    obj = ObservationManager('cv', str(obs_file))
    mask = obj._classify_basic_mask(cat.category_bits)
    compare = obj._mask_cloud_bits(mask)
    x = np.array([[0, 0, 0, 1, 1, 1],
                  [0, 1, 0, 1, 0, 1]])
    testing.assert_array_almost_equal(x, compare)


def test_check_rainrate(obs_file):
    obj = ObservationManager('cv', str(obs_file))
    x = obj._check_rainrate()
    assert x is True


def test_get_rainrate_threshold(obs_file):
    obj = ObservationManager('cv', str(obs_file))
    x = obj._get_rainrate_threshold()
    assert x == 2


def test_rain_index(obs_file):
    obj = ObservationManager('cv', str(obs_file))
    x = obj._rain_index()
    compare = np.array([0, 0, 0, 0, 1, 1], dtype=bool)
    testing.assert_array_almost_equal(x, compare)
