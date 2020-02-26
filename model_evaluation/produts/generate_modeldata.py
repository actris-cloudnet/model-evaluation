"""
TODO: Modify names of quantities from cycle files

This file will gather and connect model data from  all the model from select
level3 quantity.

gets: L3 product name, L3 obs. file
Creates or adds data to .nc file
"""
import os
import configparser
import importlib
from model_evaluation.file_handler import DataSource, update_attributes, save_model_file, add_var2ncfile
from model_evaluation.metadata import L3_ATTRIBUTES

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


def generate_model_data(model, model_files, output_file, product=None):
    """Gathers model information for site from config.ini.
    Generates all products in one model file. Creates file if not existing

    Args:
        model (str): name of model
        model_files (list): List of files from model to be generated
        output_file (str): name of model output file
        product (str, option): Name of product to generate for model and add to file.
        If none, gets list of all product to be generated and added to file.
    """
    is_file = os.path.isfile(output_file)
    for m_file in model_files:
        model_data = ModelDataHandler(m_file, model, is_file, product)
        update_attributes(model_data.data, L3_ATTRIBUTES)

        if os.path.isfile(output_file) is False:
            save_model_file(f"{model}_products", model_data, output_file)
            is_file = os.path.isfile(output_file)
        else:
            add_var2ncfile(model_data, output_file)


class ModelDataHandler(DataSource):
    """Creates and modifies L2b files for model.
        File includes all L3 products calculated per model data.
        File includes also all necessary data for model cycles.
    """
    def __init__(self, model_file, model, is_file, product=None):
        super().__init__(model_file)
        self.model = model
        self.product = product
        self.is_file = is_file
        self.cycle = self._read_cycle_name(model_file)
        self.generate_products()
        self.add_variables()

    def _read_cycle_name(self, model_file):
        """Get cycle name from config for savin variable name"""
        cycles = CONF[self.model]['cycle']
        for cycle in cycles.split(', '):
            if cycle in model_file:
                return f"_{cycle}"
        return ""

    def generate_products(self):
        cls = getattr(importlib.import_module(__name__), 'ModelDataHandler')
        if not self.product:
            f_products = [i for i in dir(cls) if i.startswith('_get_')]
            for func in f_products:
                getattr(cls, func)(self)
        elif type(self.product) is list:
            for p in self.product:
                try:
                    getattr(cls, f"_get_{p}")(self)
                except RuntimeError as error:
                    print(error)
        else:
            try:
                getattr(cls, f"_get_{self.product}")(self)
            except RuntimeError as error:
                print(error)

    # TODO: Should these _get_productX be connected into one?
    def _get_cv(self):
        """Collect cloud fraction straight from model file."""
        cv_name = self._read_config('cv')
        cv = self._set_variables(cv_name)
        self.append_data(cv, f'{self.model}_cv{self.cycle}')

    def _get_iwc(self):
        p_name, T_name, iwc_name = self._read_config('p', 'T', 'iwc')
        p, T, qi = self._set_variables(p_name, T_name, iwc_name)
        iwc = qi * p / (287 * T)
        self.append_data(iwc, f'{self.model}_iwc{self.cycle}')

    def _get_lwc(self):
        p_name, T_name, lwc_name = self._read_config('p', 'T', 'lwc')
        p, T, ql = self._set_variables(p_name, T_name, lwc_name)
        lwc = ql * p / (287 * T)
        self.append_data(lwc, f'{self.model}_lwc{self.cycle}')

    @staticmethod
    def _read_config(*args):
        var = []
        for arg in args:
            try:
                name = CONF['model_quantity'][arg]
            except KeyError:
                print(f"Wrong name: {KeyError}")
            var.append(name)
        if len(var) == 1:
            return var[0]
        return var

    def _set_variables(self, *args):
        var = []
        for arg in args:
            var.append(self.getvar(arg))
        if len(var) == 1:
            return var[0]
        return var

    def add_variables(self):
        """Add basic variables off model and cycle"""
        def add_cycle_variables():
            wanted_vars = CONF['model_wanted_vars']['cycle']
            for var in wanted_vars.split(', '):
                if var in self.dataset.variables:
                    self.append_data(self.dataset.variables[var][:], f"{self.model}_{var}{self.cycle}")

        def add_common_variables():
            wanted_vars = CONF['model_wanted_vars']['common']
            for var in wanted_vars.split(', '):
                if var in self.dataset.variables:
                    self.append_data(self.dataset.variables[var][:], f"{var}")

        if self.is_file is False:
            add_common_variables()
        if not self.product:
            add_cycle_variables()
