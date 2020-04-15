import os
import configparser
import importlib
from cloudnetpy.utils import isscalar
from cloudnetpy.categorize.datasource import DataSource

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


class ModelGrid(DataSource):
    """ Generates model data to L2b products.

    Args:
        model_file (DataSource): The :class:'DataSource' instance.
        model (str): Name of model
        output_file (str): name of output file to save data
        product (str): name of product to generate
    """
    def __init__(self, model_file, model, output_file, product):
        super().__init__(model_file)
        self._model = model
        self._product = product
        self.keys = {}
        self._is_file = os.path.isfile(output_file)
        self._cycle = self._read_cycle_name(model_file)
        self._add_variables()
        self._generate_products()

    def _read_cycle_name(self, model_file):
        """Get cycle name from config for savin variable name"""
        cycles = CONF[self._model]['cycle']
        for cycle in cycles.split(', '):
            if cycle in model_file:
                return f"_{cycle}"
        return ""

    def _generate_products(self):
        cls = getattr(importlib.import_module(__name__), 'ModelGrid')
        try:
            getattr(cls, f"_get_{self._product}")(self)
        except RuntimeError as error:
            print(error)

    def _get_cv(self):
        """Collect cloud fraction straight from model file."""
        cv_name = self._read_config('cv')
        cv = self._set_variables(cv_name)
        cv = self.cut_off_extra_levels(cv)
        self.append_data(cv, f'{self._model}_cv{self._cycle}')
        self.keys[self._product] = f'{self._model}_cv{self._cycle}'

    def _get_iwc(self):
        p_name, T_name, iwc_name = self._read_config('p', 'T', 'iwc')
        p, T, qi = self._set_variables(p_name, T_name, iwc_name)
        iwc = self._calc_water_content(qi, p, T)
        iwc = self.cut_off_extra_levels(iwc)
        self.append_data(iwc, f'{self._model}_iwc{self._cycle}')
        self.keys[self._product] = f'{self._model}_iwc{self._cycle}'

    def _get_lwc(self):
        p_name, T_name, lwc_name = self._read_config('p', 'T', 'lwc')
        p, T, ql = self._set_variables(p_name, T_name, lwc_name)
        lwc = self._calc_water_content(ql, p, T)
        lwc = self.cut_off_extra_levels(lwc)
        self.append_data(lwc, f'{self._model}_lwc{self._cycle}')
        self.keys[self._product] = f'{self._model}_lwc{self._cycle}'

    @staticmethod
    def _read_config(*args):
        var = []
        for arg in args:
            var.append(CONF['model_quantity'][arg])
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

    @staticmethod
    def _calc_water_content(q, p, T):
        return q * p / (287 * T)

    def _add_variables(self):
        """Add basic variables off model and cycle"""
        def _add_common_variables():
            wanted_vars = CONF['model_wanted_vars']['common']
            for var in wanted_vars.split(', '):
                if var in self.dataset.variables:
                    data = self.dataset.variables[var][:]
                    if isscalar(data) is False and len(data) > 25:
                        data = self.cut_off_extra_levels(self.dataset.variables[var][:])
                    self.append_data(data, f"{var}")

        def _add_cycle_variables():
            wanted_vars = CONF['model_wanted_vars']['cycle']
            for var in wanted_vars.split(', '):
                if var in self.dataset.variables:
                    data = self.dataset.variables[var][:]
                    if data.ndim > 1 or len(data) > 25:
                        data = self.cut_off_extra_levels(self.dataset.variables[var][:])
                    self.append_data(data, f"{self._model}_{var}{self._cycle}")
                if var == 'height':
                    self.keys['height'] = f"{self._model}_{var}{self._cycle}"
        if self._is_file is False:
            _add_common_variables()
        _add_cycle_variables()

    def cut_off_extra_levels(self, data):
        """ Remove unused levels from model data"""
        level = int(CONF[self._model]['level'])
        if data.ndim > 1:
            data = data[:, :level]
        else:
            data = data[:level]
        return data
