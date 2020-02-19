"""
TODO: better file name

This file will gather and connect model data from  all the model from select
level3 quantity.

gets: L3 product name, L3 obs. file
Creates or adds data to .nc file
"""
import os
import configparser
import importlib
from model_evaluation.file_handler import DataSource, update_attributes, save_model_file
from model_evaluation.metadata import L3_ATTRIBUTES

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


def generate_model_data(model, model_file, output_file, product=None):
    """Gathers model information for site from config.ini.
    Generates all products in one model file. Creates file if not existing

    Args:
        site (str): Name of site
        model (str): name of model
        model_file (str): file path of model to be generated
        product (str, option): Name of product to generate for model and add to file.
        If none, gets list of all product to be generated and added to file.
        # Mitä tehdään, jos useampi tuote halutaan generoida kerralla?
    """
    model_data = ModelDataHandler(model_file, model, product)
    update_attributes(model_data.data, L3_ATTRIBUTES)
    save_model_file(f"{model}_products", model_data, output_file)


class ModelDataHandler(DataSource):
    """Creates and modifies L2b files for model.
        File includes all L3 products calculated per model data.
        File includes also all necessary data for model cycles.
    """
    def __init__(self, model_file, model, product=None):
        super().__init__(model_file)
        self.model = model
        self.product = product
        self.generate_products()
        self.add_variables()

    def generate_products(self):
        module = importlib.import_module(__name__)
        print(module)
        if not self.product:
            # Ehkä tässä voisi samalla tyylillä hakea kaikki get tyyppiset funktiot?
            self._get_cloud_fraction()
            #self._get_iwc()
            #self._get_lwc()
        else:
            try:
                getattr(module, f"_get_{self.product}")
            except RuntimeError as error:
                print(error)

    def add_variables(self):
        """Add variables connect to model and cycle"""
        def add_cycle_variables():
            wanted_vars = CONF['model_wanted_vars']['cycle']
            for var in wanted_vars.split(', '):
                if var in self.dataset.variables:
                    self.append_data(self.dataset.variables[var][:], f"{self.model}_{var}")

        def add_common_variables():
            wanted_vars = CONF['model_wanted_vars']['common']
            for var in wanted_vars.split(', '):
                if var in self.dataset.variables:
                    self.append_data(self.dataset.variables[var][:], f"{var}")

        add_common_variables()
        add_cycle_variables()

    def _get_cloud_fraction(self):
        """Collect cloud fraction straight from model file."""
        cv_name = CONF[self.model]['cv']
        cv = self.getvar(cv_name)
        self.append_data(cv, f'{self.model}_cv')

    def _get_iwc(self):
        p_name, T_name, iwc_name = self._read_common_quantities('iwc')
        p, T, qi = self.getvar(p_name, T_name, iwc_name)
        iwc = qi * p / (287 * T)
        self.append_data(iwc, f'{self.model}_iwc')

    def _get_lwc(self):
        p_name, T_name, lwc_name = self._read_common_quantities('lwc')
        p, T, ql = self.getvar(p_name, T_name, lwc_name)
        lwc = ql * p / (287 * T)
        self.append_data(lwc, f'{self.model}_iwc')

    def _read_common_quantities(self, var):
        try:
            p_name = CONF[self.model]['p']
        except KeyError:
            p_name = CONF['general']['p']
        try:
            T_name = CONF[self.model]['T']
        except KeyError:
            T_name = CONF['general']['T']
        var_name = CONF[self.model][var]
        return p_name, T_name, var_name
