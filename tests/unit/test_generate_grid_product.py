import numpy as np
from model_evaluation.products.generate_grid_product import ObservationManager
from model_evaluation.products.model_products import ModelGrid


MODEL = 'ecmwf'
OUTPUT_FILE = '/home/korpinen/Documents/ACTRIS/model_evaluation/test_data_ecmwf.nc'
PRODUCT = 'iwc'


class CategorizeBits:
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
                                                    [0, 0, 1, 0, 0, 0]], dtype=bool),
                              }
        self.quality_bits = {'radar': np.asarray([[0, 0, 0, 1, 1, 1],
                                                  [1, 0, 0, 1, 1, 1]], dtype=bool),
                             'lidar': np.asarray([[1, 1, 1, 1, 0, 0],
                                                  [1, 1, 0, 1, 1, 0]], dtype=bool),
                             'clutter': np.asarray([[0, 0, 1, 1, 0, 0],
                                                    [0, 0, 0, 0, 0, 0]], dtype=bool),
                             'molecular': np.asarray([[1, 0, 0, 1, 0, 0],
                                                      [0, 1, 0, 0, 0, 0]], dtype=bool),
                             'attenuated': np.asarray([[1, 1, 1, 0, 0, 1],
                                                       [0, 1, 1, 0, 0, 0]], dtype=bool),
                             'corrected': np.asarray([[1, 0, 0, 0, 0, 0],
                                                      [1, 1, 0, 0, 0, 0]], dtype=bool)}


def test_regridded_array(model_file, obs_file):
    m_obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    o_obj= ObservationManager(PRODUCT, str(obs_file))
    assert True


def test_time2datetime():
    assert True


def test_get_date():
    assert True


def test_generate_product():
    assert True


def test_generate_cv():
    assert True


def test_get_rainrate_threshold():
    assert True


def test_rain_index():
    assert True
