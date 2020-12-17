import os
import configparser
import importlib
import numpy as np
import numpy.ma as ma
from cloudnetpy.utils import isscalar
from cloudnetpy.categorize.datasource import DataSource

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


class ModelManager(DataSource):
    """Class to collect and manage model data.

    Args:
        model_file (str): Path to source model file.
        model (str): Name of model
        output_file (str): name of output file to save data
        product (str): name of product to generate

    Notes:
        Output_file is given for saving all cycles to same nc-file. Some variables
        are same in control run and cycles so checking existence of output-file
        prevents duplicates as well as unnecessary processing.

        Class inherits DataSource interface from CloudnetPy.
    """
    def __init__(self, model_file: str, model: str,
                 output_file: str, product: str):
        super().__init__(model_file)
        self.model = model
        self._product = product
        self.keys = {}
        self._is_file = os.path.isfile(output_file)
        self._cycle = self._read_cycle_name(model_file)
        self._add_variables()
        self._generate_products()
        self.date = []
        self.wind = self._calculate_wind_speed()
        self.resolution_h = self._set_variables('horizontal_resolution')

    def _read_cycle_name(self, model_file: str):
        """Get cycle name from config for saving variable name"""
        cycles = CONF[self.model]['cycle']
        cycles = [x.strip() for x in cycles.split(',')]
        for cycle in cycles:
            if cycle in model_file:
                return f"_{cycle}"
        return ""

    def _generate_products(self):
        cls = getattr(importlib.import_module(__name__), 'ModelManager')
        try:
            getattr(cls, f"_get_{self._product}")(self)
        except RuntimeError as error:
            print(error)

    def _get_cf(self):
        """Collect cloud fraction straight from model file."""
        cf_name = self._read_config('cf')
        cf = self._set_variables(cf_name)
        cf = self._cut_off_extra_levels(cf)
        cf[cf < 0] = ma.masked
        self.append_data(cf, f'{self.model}_cf{self._cycle}')
        self.keys[self._product] = f'{self.model}_cf{self._cycle}'

    def _get_iwc(self):
        p_name, T_name, iwc_name = self._read_config('p', 'T', 'iwc')
        p, T, qi = self._set_variables(p_name, T_name, iwc_name)
        iwc = self._calc_water_content(qi, p, T)
        iwc = self._cut_off_extra_levels(iwc)
        iwc[iwc < 0] = ma.masked
        self.append_data(iwc, f'{self.model}_iwc{self._cycle}')
        self.keys[self._product] = f'{self.model}_iwc{self._cycle}'

    def _get_lwc(self):
        p_name, T_name, lwc_name = self._read_config('p', 'T', 'lwc')
        p, T, ql = self._set_variables(p_name, T_name, lwc_name)
        lwc = self._calc_water_content(ql, p, T)
        lwc = self._cut_off_extra_levels(lwc)
        lwc[lwc < 0] = ma.masked
        self.append_data(lwc, f'{self.model}_lwc{self._cycle}')
        self.keys[self._product] = f'{self.model}_lwc{self._cycle}'

    @staticmethod
    def _read_config(*args: str):
        var = []
        for arg in args:
            var.append(CONF['model_quantity'][arg])
        if len(var) == 1:
            return var[0]
        return var

    def _set_variables(self, *args: str):
        var = []
        for arg in args:
            var.append(self.getvar(arg))
        if len(var) == 1:
            return var[0]
        return var

    @staticmethod
    def _calc_water_content(q: float, p: float, T: float):
        return q * p / (287 * T)

    def _add_variables(self):
        """Add basic variables off model and cycle"""
        def _add_common_variables():
            wanted_vars = CONF['model_wanted_vars']['common']
            wanted_vars = [x.strip() for x in wanted_vars.split(',')]
            for var in wanted_vars:
                if var in self.dataset.variables:
                    data = self.dataset.variables[var][:]
                    if not isscalar(data) and len(data) > 25:
                        data = self._cut_off_extra_levels(self.dataset.variables[var][:])
                    self.append_data(data, f"{var}")

        def _add_cycle_variables():
            wanted_vars = CONF['model_wanted_vars']['cycle']
            wanted_vars = [x.strip() for x in wanted_vars.split(',')]
            for var in wanted_vars:
                if var in self.dataset.variables:
                    data = self.dataset.variables[var][:]
                    if data.ndim > 1 or len(data) > 25:
                        data = self._cut_off_extra_levels(self.dataset.variables[var][:])
                    self.append_data(data, f"{self.model}_{var}{self._cycle}")
                if var == 'height':
                    self.keys['height'] = f"{self.model}_{var}{self._cycle}"
        if not self._is_file:
            _add_common_variables()
        _add_cycle_variables()

    def _cut_off_extra_levels(self, data: np.ndarray):
        """ Remove unused levels from model data"""
        level = int(CONF[self.model]['level'])
        if data.ndim > 1:
            data = data[:, :level]
        else:
            data = data[:level]
        return data

    def _calculate_wind_speed(self):
        """Real wind from x- and y-components"""
        u = self._set_variables('uwind')
        v = self._set_variables('vwind')
        u = self._cut_off_extra_levels(u)
        v = self._cut_off_extra_levels(v)
        return np.sqrt(u.data**2 + v.data**2)
