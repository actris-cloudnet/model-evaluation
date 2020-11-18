import numpy as np
import numpy.ma as ma
import numpy.testing as testing
import pytest
from model_evaluation.products.model_products import ModelManager
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.grid_methods import ProductGrid

MODEL = 'ecmwf'
OUTPUT_FILE = ''
PRODUCT = 'iwc'


def test_generate_regrid_product(model_file, obs_file):
    # Voi testaa, tuleeko kaikki halutut tuotteet olioon
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    assert True


@pytest.mark.parametrize("key, value",[
    ("iwc", 3), ("lwc", 1), ("cf", 2)])
def test_get_method_storage(key, value, model_file, obs_file):
    obs = ObservationManager(key, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, key)
    obj = ProductGrid(model, obs)
    x, y = obj._get_method_storage()
    assert len(x.keys()) == value


@pytest.mark.parametrize("key, value",[
    ("iwc", 3), ("lwc", 1), ("cf", 2)])
def test_get_method_storage_adv(key, value, model_file, obs_file):
    obs = ObservationManager(key, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, key)
    obj = ProductGrid(model, obs)
    x, y = obj._get_method_storage()
    assert len(y.keys()) == value


@pytest.mark.parametrize("name", ['cf_V', 'cf_A'])
def test_cf_method_storage(name, model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    x, y = obj._cf_method_storage()
    assert name in x.keys()


@pytest.mark.parametrize("name", ['cf_V_adv', 'cf_A_adv'])
def test_cf_method_storage_adv(name, model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    x, y = obj._cf_method_storage()
    assert name in y.keys()


@pytest.mark.parametrize("name",
    ['iwc', 'iwc_att', 'iwc_rain'])
def test_iwc_method_storage(name, model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    x, y = obj._iwc_method_storage()
    assert name in x.keys()


@pytest.mark.parametrize("name",
    ['iwc_adv', 'iwc_att_adv', 'iwc_rain_adv'])
def test_iwc_method_storage_adv(name, model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    x, y = obj._iwc_method_storage()
    assert name in y.keys()


def test_product_method_storage(model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj = ProductGrid(model, obs)
    x, y = obj._product_method_storage()
    assert 'lwc' in x.keys()


def test_product_method_storage_adv(model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj = ProductGrid(model, obs)
    x, y = obj._product_method_storage()
    assert 'lwc_adv' in y.keys()


def test_regrid_cf_area(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 0]])
    dict = {'cf_A': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_A']
    compare = np.mean(np.sum(data, 1) > 0)
    assert x[0, 0] == compare


def test_regrid_cf_none(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = None
    dict = {'cf_A': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_A']
    assert np.isnan(x[0, 0])


def test_regrid_cf_area_masked(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = ma.array([[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 0]])
    data[1,:] = ma.masked
    dict = {'cf_A': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_A']
    compare = np.mean(np.sum(data, 1) > 0)
    assert x[0, 0] == compare


def test_regrid_cf_area_nan(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = np.array([[1, np.nan, 1], [0, 1, 1], [np.nan, 0, 1], [0, 0, 0]])
    dict = {'cf_A': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_A']
    compare = np.nanmean(np.nansum(data, 1) > 0)
    assert x[0, 0] == compare


def test_regrid_cf_volume(model_file, obs_file):
    # Testataa, jos ei saa _A_:ta palauttaa keskiarvon
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 0]])
    dict = {'cf_V': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_V']
    compare = np.mean(data)
    assert x[0, 0] == compare


def test_regrid_cf_volume_nan(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = np.array([[1, np.nan, 1], [0, 1, 1], [np.nan, 0, 1], [0, 0, 0]])
    dict = {'cf_V': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_V']
    compare = np.nanmean(data)
    assert x[0, 0] == compare


def test_regrid_cf_volume_masked(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    data = ma.array([[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 0]])
    data[1, :] = ma.masked
    dict = {'cf_V': np.zeros((1, 1))}
    dict = obj._regrid_cf(dict, 0, 0, data)
    x = dict['cf_V']
    compare = np.mean(data)
    assert x[0, 0] == compare


def test_reshape_data_to_window(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    xnd = np.array([1, 1, 1, 0, 0, 0])
    ynd = np.array([1, 1, 0, 0])
    ind = np.array([[1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]], dtype=bool)
    obj._obs_data = np.array([[1, 2, 3, 4],
                              [11, 22, 33, 44],
                              [111, 222, 333, 444],
                              [5, 6, 7, 8],
                              [55, 66, 77, 88],
                              [555, 666, 777, 888]])
    x = obj._reshape_data_to_window(ind, xnd, ynd)
    compare = np.array([[1, 2], [11, 22], [111, 222]])
    testing.assert_array_almost_equal(x, compare)


def test_reshape_data_to_window_middle(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    xnd = np.array([0, 0, 1, 1, 1, 0])
    ynd = np.array([0, 1, 1, 0])
    ind = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]], dtype=bool)
    obj._obs_data = np.array([[1, 2, 3, 4],
                              [11, 22, 33, 44],
                              [111, 222, 333, 444],
                              [5, 6, 7, 8],
                              [55, 66, 77, 88],
                              [555, 666, 777, 888]])
    x = obj._reshape_data_to_window(ind, xnd, ynd)
    compare = np.array([[222, 333], [6, 7], [66, 77]])
    testing.assert_array_almost_equal(x, compare)


def test_reshape_data_to_window_empty(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    xnd = np.array([1, 1, 1, 0, 0, 0, ])
    ynd = np.array([0, 0, 0, 0])
    ind = np.array([1, 1, 0, 0], dtype=bool)
    x = obj._reshape_data_to_window(ind, xnd, ynd)
    assert x is None


def test_regrid_iwc(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, 1, 1],
                              [2, 2, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 3]])
    dict = {'iwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_nan(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, np.nan, 1],
                              [2, np.nan, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, np.nan]])
    dict = {'iwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_masked(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, 1, 1],
                              [2, 2, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 4]])
    obj._obs_data[1, :] = ma.masked
    dict = {'iwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_none(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, 1, 1],
                              [2, 2, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 4]])
    dict = {'iwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc']
    testing.assert_equal(x[0, 0], compare)


def test_regrid_iwc_att(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    dict = {'iwc_att': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_obj.data['iwc_att'][:][no_rain])
    x = dict['iwc_att']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_att_masked(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_obj.data['iwc_att'][:].mask = ma.array([[1, 0, 1, 0],
                                                     [0, 1, 1, 0],
                                                     [1, 0, 0, 1],
                                                     [0, 1, 1, 1],
                                                     [1, 1, 0, 0],
                                                     [0, 1, 0, 1]], dtype=bool)
    dict = {'iwc_att': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 1, 1, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_obj.data['iwc_att'][:][no_rain])
    x = dict['iwc_att']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_att_none(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    dict = {'iwc_att': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    x = dict['iwc_att']
    assert np.isnan(x[0, 0])


def test_regrid_iwc_rain(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, 1, 1],
                              [2, 2, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 3]])
    dict = {'iwc_rain': np.zeros((1, 1))}
    ind = np.array([[1, 0, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 1, 1, 1],
                    [0, 0, 1, 1]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc_rain']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_rain_nan(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, np.nan, 1, 1],
                              [2, 2, 2, np.nan],
                              [3, 3, 3, 3],
                              [np.nan, 4, 4, np.nan]])
    dict = {'iwc_rain': np.zeros((1, 1))}
    ind = np.array([[1, 0, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 1, 1, 1],
                    [0, 0, 1, 1]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc_rain']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_iwc_rain_masked(model_file, obs_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 3, 1, 1],
                              [2, 2, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 4]])
    obj._obs_data[2, :] = ma.masked
    dict = {'iwc_rain': np.zeros((1, 1))}
    ind = np.array([[1, 0, 1, 1]], dtype=bool)
    no_rain = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 1, 1, 1],
                    [0, 0, 1, 1]], dtype=bool)
    dict = obj._regrid_iwc(dict, 0, 0, ind, no_rain)
    compare = np.nanmean(obj._obs_data[no_rain])
    x = dict['iwc_rain']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_product(model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj = ProductGrid(model, obs)
    obj._obs_data = np.array([[1, 1, 1, 1],
                              [2, 1, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 4]])
    dict = {'lwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_product(dict, 0, 0, ind)
    compare = np.nanmean(obj._obs_data[ind])
    x = dict['lwc']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_product_nan(model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj = ProductGrid(model, obs)
    obj._obs_data = np.array([[1, np.nan, 1, 1],
                              [np.nan, 1, 2, 2],
                              [3, 3, np.nan, 3],
                              [4, np.nan, 4, 4]])
    dict = {'lwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_product(dict, 0, 0, ind)
    compare = np.nanmean(obj._obs_data[ind])
    x = dict['lwc']
    testing.assert_almost_equal(x[0, 0], compare)


def test_regrid_product_masked(model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, 1, 1],
                              [2, 1, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 4]])
    obj._obs_data[2, :] = ma.masked
    dict = {'lwc': np.zeros((1, 1))}
    ind = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_product(dict, 0, 0, ind)
    compare = np.nanmean(obj._obs_data[ind])
    x = dict['lwc']
    testing.assert_almost_equal(x[0, 0], compare)



def test_regrid_product_none(model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    obj = ProductGrid(model, obs)
    obj._obs_data = ma.array([[1, 1, 1, 1],
                              [2, 1, 2, 2],
                              [3, 3, 3, 3],
                              [4, 4, 4, 4]])
    dict = {'lwc': np.zeros((1, 1))}
    ind = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]], dtype=bool)
    dict = obj._regrid_product(dict, 0, 0, ind)
    compare = np.nanmean(obj._obs_data[ind])
    x = dict['lwc']
    testing.assert_almost_equal(x[0, 0], compare)


@pytest.mark.parametrize("product", [
    "cf_A", "cf_V", "cf_A_adv", "cf_V_adv"])
def test_append_data2object_cf(product, model_file, obs_file):
    obs = ObservationManager('cf', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'cf')
    ProductGrid(model, obs, MODEL, 'cf')
    assert product + '_' + MODEL in model.data.keys()


@pytest.mark.parametrize("product", [
    "iwc", "iwc_mask", "iwc_att", "iwc_rain",
    "iwc_adv", "iwc_mask_adv", "iwc_att_adv", "iwc_rain_adv"])
def test_append_data2object_cf(product, model_file, obs_file):
    obs = ObservationManager('iwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'iwc')
    ProductGrid(model, obs, MODEL, 'iwc')
    assert product + '_' + MODEL in model.data.keys()


@pytest.mark.parametrize("product", [
    "lwc", "lwc_adv"])
def test_append_data2object_cf(product, model_file, obs_file):
    obs = ObservationManager('lwc', str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, 'lwc')
    ProductGrid(model, obs)
    assert product + '_' + MODEL in model.data.keys()
