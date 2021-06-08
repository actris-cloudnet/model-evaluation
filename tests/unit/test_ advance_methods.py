import numpy as np
import numpy.testing as testing
import pytest
from model_evaluation.products.model_products import ModelManager
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.advance_methods import AdvanceProductMethods

MODEL = 'ecmwf'
OUTPUT_FILE = ''
PRODUCT = 'cf'


def test_cf_cirrus_filter(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # Katotaan, että löytyy luotu muuttuja...
    # Ehkä voidaan varmistaa, että on eroja / ei ole eroja
    assert True


def test_getvar_from_object(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # Annetaan jokin otus, jonka löytää suoraan, löytää osan, ei löydä
    assert True


def test_remove_extra_levels(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # Tsekkaa alun ja lopun shape ero
    assert True


def test_set_frequency_parameters(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # Annetaan eri taajuus ja katotaan, että halutut luvut tulee ulos.
    assert True


def test_fit_z_sensitivity(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # z_zensitive tärkein, varmistetaan että interpolointi menee oikein
    # Muut on vain arvoja
    assert True


def test_filter_high_iwc_low_cf(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_mask_weird_indices(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # Testaa, että weird indekit menee oikein
    assert True


def find_ice_in_clouds(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_get_ice_indices(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_iwc_variance(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_calculate_variance_iwc(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_calculate_wind_shear(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    # Selkeä, testataan, että tuuliväänteestä tulee halutunlainen
    assert True


def test_calculate_iwc_distribution(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_gamma_distribution(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_get_observation_index(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)
    assert True


def test_filter_cirrus(obs_file, model_file):
    obs = ObservationManager(PRODUCT, str(obs_file))
    model = ModelManager(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    adv_pro = AdvanceProductMethods(model, str(model_file), obs)

    assert True
