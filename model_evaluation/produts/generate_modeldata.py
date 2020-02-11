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


def generate_model_data(site, model_file, model, product=None):
    """Gathers model information for site from config.ini.
    Generates all products in one model file. Creates file if not existing

    Args:
        site (str): Name of site
        model_file (str): file path of model to be generated
        product (str, option): Name of product to generate for model and add to file.
        If none, gets list of all product to be generated and added to file.
    """
    # Luetaan configsta, mitä malleja sitelle löytyy
    # Luokka, jolla luetaan mallidata loopissa ja lasketaan tarvittaessa tuote
    # Luodaan tiedosto, lisätään muuttujat sinne
    # Malli filuun pitää ehkä saada kopioitua metaa myös havainto-filusta

    if not product:
        product = CONF['products']['product']


class ModelDataHandler(DataSource):
    """Creates and modifies L2b files for model.
        File includes all L3 products calculated per model data.
        File includes also all necessary data for model cycles.
    """
    def __init__(self, model_file, model):
        super().__init__(model_file)
        self.model = model

    def get_cloud_fraction(self):
        """Collect cloud fraction straight from model file."""
        cv_name = CONF[self.model]['cv']
        cv = self.getvar(cv_name)
        self.append_data(f'{self.model}_cv', cv)

    # Näissä jo nyt aika paljon samaa, mietitään fiksummaksi, kunhan toimii
    def get_iwc(self):
        print("lol")
        p_name = CONF[self.model]['pressure']
        T_name = CONF[self.model]['Temperature']
        iwc_name = CONF[self.model]['iwc']
        p, T, qi = self.getvar(p_name, T_name, iwc_name)
        iwc = qi * p / (287*T)
        self.append_data(f'{self.model}_iwc', iwc)

    def get_lwc(self):
        p_name = CONF[self.model]['pressure']
        T_name = CONF[self.model]['Temperature']
        lwc_name = CONF[self.model]['lwc']
        p, T, ql = self.getvar(p_name, T_name, lwc_name)
        lwc = ql * p / (287 * T)
        self.append_data(f'{self.model}_iwc', lwc)
