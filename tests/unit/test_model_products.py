import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import numpy.testing as testing
import pytest
import netCDF4
from model_evaluation.products.model_products import ModelGrid

root = os.path.split(os.path.split(Path(__file__).parent)[0])[0]

MODEL = 'ecmwf'
OUTPUT_FILE = f'{root}/test_files/test_data_ecmwf_iwc.nc'
PRODUCT = 'iwc'


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


def test_cut_off_extra_level(model_file):
    obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    data = np.array([np.arange(100), np.arange(100)])
    compare = np.array([np.arange(88), np.arange(88)])
    x = obj.cut_off_extra_levels(data)
    testing.assert_array_almost_equal(x, compare)
