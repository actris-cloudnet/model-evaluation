import os
import importlib
from typing import Union
import numpy as np
import numpy.ma as ma
import logging
from cloudnetpy.utils import isscalar
from cloudnetpy.categorize.datasource import DataSource
from model_evaluation.model_metadata import MODELS, VARIABLES
from model_evaluation.utils import file_exists


class ModelManager(DataSource):
    """Class to collect and manage model data.

    Args:
        model_file (str): Path to source model file.
        model (str): Name of model
        output_file (str): name of output file name and path to save data
        product (str): name of product to generate

    Notes:
        For this class to work, needed information of model in use should be found in
        model_metadata.py

        Output_file is given for saving all cycles to same nc-file. Some variables
        are same in control run and cycles so checking existence of output-file
        prevents duplicates as well as unnecessary processing.

        Class inherits DataSource interface from CloudnetPy.
    """
    def __init__(self, model_file: str, model: str,
                 output_file: str, product: str, check_file: bool = True):
        super().__init__(model_file)
        self.model = model
        self.model_info = MODELS[model]
        self.model_vars = VARIABLES['variables']
        self._product = product
        self.keys = {}
        self._is_file = file_exists(output_file) if check_file else False
        self._cycle = self._read_cycle_name(model_file)
        self._add_variables()
        self._generate_products()
        self.date = []
        self.wind = self._calculate_wind_speed()
        self.resolution_h = self._get_horizontal_resolution()

    def _read_cycle_name(self, model_file: str):
        """Get cycle name from model_metadata.py for saving variable name(s)"""
        try:
            cycles = self.model_info.cycle
            cycles = [x.strip() for x in cycles.split(',')]
            for cycle in cycles:
                if cycle in model_file:
                    return f"_{cycle}"
        except AttributeError:
            return ""

    def _generate_products(self):
        """Process needed data of model to a ModelManager object"""
        cls = getattr(importlib.import_module(__name__), 'ModelManager')
        try:
            getattr(cls, f"_get_{self._product}")(self)
        except AttributeError as e:
            logging.error(f'Invalid product name: {e}')
            raise

    def _get_cf(self):
        """Collect cloud fraction straight from model file."""
        cf_name = self._get_model_var_names('cf')
        cf = self._set_variables(cf_name)
        cf = self._cut_off_extra_levels(cf)
        cf[cf < 0.05] = ma.masked
        self.append_data(cf, f'{self.model}{self._cycle}_cf')
        self.keys[self._product] = f'{self.model}{self._cycle}_cf'

    def _get_iwc(self):
        iwc = self._get_water_continent('iwc')
        self.append_data(iwc, f'{self.model}{self._cycle}_iwc')
        self.keys[self._product] = f'{self.model}{self._cycle}_iwc'

    def _get_lwc(self):
        lwc = self._get_water_continent('lwc')
        self.append_data(lwc, f'{self.model}{self._cycle}_lwc')
        self.keys[self._product] = f'{self.model}{self._cycle}_lwc'

    @staticmethod
    def _get_model_var_names(*args: Union[str, list]) -> list:
        var = []
        for arg in args:
            var.append(VARIABLES[arg].long_name)
        if len(var) == 1:
            return var[0]
        return var

    def _set_variables(self, *args: Union[str, list]) -> Union[np.array, list]:
        var = []
        for arg in args:
            var.append(self.getvar(arg))
        if len(var) == 1:
            return var[0]
        return var

    def _get_water_continent(self, var: str) -> np.array:
        p_name, T_name, lwc_name = self._get_model_var_names('p', 'T', var)
        p, T, q = self._set_variables(p_name, T_name, lwc_name)
        wc = self._calc_water_content(q, p, T)
        wc = self._cut_off_extra_levels(wc)
        wc[wc < 0.0] = ma.masked
        return wc

    @staticmethod
    def _calc_water_content(q: np.array, p: np.array, T: np.array) -> np.array:
        return q * p / (287 * T)

    def _add_variables(self):
        """Add basic variables off model and cycle"""
        def _add_common_variables():
            """Model variables that are always the same within cycles"""
            wanted_vars = self.model_vars.common_var
            wanted_vars = [x.strip() for x in wanted_vars.split(',')]
            for var in wanted_vars:
                if var in self.dataset.variables:
                    data = self.dataset.variables[var][:]
                    if not isscalar(data) and len(data) > 25:
                        data = self._cut_off_extra_levels(self.dataset.variables[var][:])
                    self.append_data(data, f"{var}")

        def _add_cycle_variables():
            """Add cycle depending variables"""
            wanted_vars = self.model_vars.cycle_var
            wanted_vars = [x.strip() for x in wanted_vars.split(',')]
            for var in wanted_vars:
                if var in self.dataset.variables:
                    data = self.dataset.variables[var][:]
                    if data.ndim > 1 or len(data) > 25:
                        data = self._cut_off_extra_levels(self.dataset.variables[var][:])
                    self.append_data(data, f"{self.model}{self._cycle}_{var}")
                if var == 'height':
                    self.keys['height'] = f"{self.model}{self._cycle}_{var}"
        if not self._is_file:
            _add_common_variables()
        _add_cycle_variables()

    def _cut_off_extra_levels(self, data: np.ndarray) -> np.array:
        """ Remove unused levels (over 22km) from model data"""
        try:
            level = self.model_info.level
        except KeyError:
            return data

        if data.ndim > 1:
            data = data[:, :level]
        else:
            data = data[:level]
        return data

    def _calculate_wind_speed(self) -> np.array:
        """Real wind from x- and y-components"""
        u = self._set_variables('uwind')
        v = self._set_variables('vwind')
        u = self._cut_off_extra_levels(u)
        v = self._cut_off_extra_levels(v)
        return np.sqrt(ma.power(u.data, 2) + ma.power(v.data, 2))

    def _get_horizontal_resolution(self) -> float:
        h_res = self._set_variables('horizontal_resolution')
        return np.unique(h_res.data)[0]
