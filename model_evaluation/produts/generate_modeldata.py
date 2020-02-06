"""
TODO: better file name

This file will gather and connect model data from  all the model from select
level3 quantity.

gets: L3 product name, L3 obs. file
Creates or adds data to .nc file


"""
import os
import configparser
from model_evaluation.file_handler import DataSource


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.read(os.path.join(PATH, '/level3.ini'))


def generate_model_data(site, product=None):
    """Gathers model information for site from config.ini.
    Generates all products in one model file. Creates file if not existing

    Args:
        site (str): Name of site
        product (str, option): Name of product to generate for model and add to file.
        If none, gets list of all product to be generated and added to file.
    """
    # Luetaan configsta, mitä malleja sitelle löytyy
    # Luokka, jolla luetaan mallidata loopissa ja lasketaan tarvittaessa tuote
    # Luodaan tiedosto, lisätään muuttujat sinne
    # Malli filuun pitää ehkä saada kopioitua metaa myös havainto-filusta


class ModelDataHandler(DataSource):
    """Creates and modifies L2b files for model.
        File includes all L3 products calculated per model data.
        File includes also all necessary data for model cycles.
    """
    def __init__(self, site, file_name):
        super().__init__(file_name)
        # Tässä käsitellään vain yksi mallitiedosto kerrallaan, ei loopata kaikkia
        self.site = site

    def read_models_from_config(self):
        self.models = CONF[self.site]['model']
