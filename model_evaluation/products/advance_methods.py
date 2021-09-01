import importlib
import numpy as np
import numpy.ma as ma
import cloudnetpy.utils as cl_tools
import logging
from typing import Union, Tuple
from scipy.special import gamma
from cloudnetpy.categorize.datasource import DataSource
from model_evaluation.products.model_products import ModelManager
from model_evaluation.products.observation_products import ObservationManager


class AdvanceProductMethods(DataSource):
    """Class that adds advance methods of product to nc-file.
        Different methods could be filtering or adding info by making
        assumptions of model or observation data.

        Args:
            model_obj (object): The :class:'ModelManager' object.
            obs_obj (object): The :class:'ObservationManager' object.
    """
    def __init__(self, model_obj: ModelManager,
                 model_file: str,
                 obs_obj: ObservationManager):
        super().__init__(model_file)
        self._obs_obj = obs_obj
        self.product = obs_obj.obs
        self._date = obs_obj.date
        self._obs_height = obs_obj.data['height'][:]
        self._obs_data = obs_obj.data[obs_obj.obs][:]
        self._model_obj = model_obj
        self._model_time = model_obj.time
        self._model_height = model_obj.data[model_obj.keys['height']][:]
        self.generate_products()

    def generate_products(self):
        cls = getattr(importlib.import_module(__name__), 'AdvanceProductMethods')
        try:
            getattr(cls, f"get_advance_{self.product}")(self)
        except AttributeError as error:
            logging.warning(f'No advance method for {self.product}: {error}')

    def get_advance_cf(self):
        self.cf_cirrus_filter()
       # Develop snow adder at some point

    def cf_cirrus_filter(self):
        cf, h = self.getvar_from_object('cf', 'h')
        T = self._model_obj._set_variables('temperature')
        T = self.remove_extra_levels(T - 273.15)
        iwc, lwc = [self._model_obj._get_water_continent(var) for var in ['iwc', 'lwc']]

        tZT, tT, tZ, t = self.set_frequency_parameters()
        z_sen = self.fit_z_sensitivity(h)
        cf_filtered = self.filter_high_iwc_low_cf(cf, iwc, lwc)
        cloud_iwc, ice_ind = self.find_ice_in_clouds(cf_filtered, iwc, lwc)
        variance_iwc = self.iwc_variance(h, ice_ind)
        for i, ind in enumerate(zip(ice_ind[0], ice_ind[-1])):
            iwc_dist = self.calculate_iwc_distribution(cloud_iwc[i], variance_iwc[i])
            # TODO: parempi nimi tälle funktiolle
            p_iwc = self.gamma_distribution(iwc_dist, variance_iwc[i], cloud_iwc[i])
            if np.sum(p_iwc) == 0 or p_iwc[-1] > 0.01*np.sum(p_iwc):
                cf_filtered[ind] = np.nan
                continue
            obs_index = self.get_observation_index(iwc_dist, tZT, tT, tZ, t, T[ind], z_sen[ind])
            cf_filtered[ind] = self.filter_cirrus(p_iwc, obs_index, cf_filtered[ind])
        cf_filtered[cf_filtered < 0.05] = ma.masked
        self._model_obj.append_data(cf_filtered, f'{self._model_obj.model}{self._model_obj._cycle}_cf_cirrus')

    def getvar_from_object(self, *args: Union[str, list]) -> list:
        var = []
        for arg in args:
            v_name = self._model_obj._get_model_var_names(arg)
            if arg == 'cf':
                v_name = arg
            var.append(self._model_obj.data[f'{self._model_obj.model}{self._model_obj._cycle}_{v_name}'][:])
        if len(var) == 1:
            return var[0]
        return var

    def remove_extra_levels(self, *args: Union[np.array, list]) -> list:
        var = []
        for arg in args:
            var.append(self._model_obj._cut_off_extra_levels(arg))
        if len(var) == 1:
            return var[0]
        return var

    def set_frequency_parameters(self) -> Tuple:
        if 30 <= self._obs_obj.radar_freq <= 40:
            return 0.000242, -0.0186, 0.0699, -1.63
        if 90 <= float(self._obs_obj.radar_freq) <= 100:
            return 0.00058, -0.00706, 0.0923, -0.992

    def fit_z_sensitivity(self, h: np.array) -> np.array:
        z_sen = [cl_tools.rebin_1d(self._obs_obj.height, self._obs_obj.z_sensitivity, h[i])
                 for i in range(len(h))]
        return np.asarray(z_sen)

    def filter_high_iwc_low_cf(self, cf: np.array, iwc: np.array, lwc: np.array) -> np.array:
        cf_filtered = self.mask_weird_indices(cf, iwc, lwc)
        if np.sum((iwc > 0) & (lwc < iwc/10) & (cf_filtered > 0)) == 0:
            raise ValueError('No ice clouds in a input data')
        return cf_filtered

    @staticmethod
    def mask_weird_indices(cf: np.array, iwc: np.array, lwc: np.array) -> np.array:
        cf_filtered = np.copy(cf)
        weird_ind = (iwc / cf > 0.5e-3) & (cf < 0.001)
        weird_ind = weird_ind | (iwc == 0) & (lwc == 0) & (cf == 0)
        cf_filtered[weird_ind] = ma.masked
        return cf_filtered

    def find_ice_in_clouds(self, cf_filtered: np.array, iwc: np.array,
                           lwc: np.array) -> Tuple[np.array, np.array]:
        ice_ind = self.get_ice_indices(cf_filtered, iwc, lwc)
        cloud_iwc = iwc[ice_ind] / cf_filtered[ice_ind] * 1e3
        return cloud_iwc, ice_ind

    @staticmethod
    def get_ice_indices(cf_filtered: np.array, iwc: np.array, lwc: np.array) -> np.array:
        return np.where((cf_filtered > 0) & (iwc > 0) & (lwc < iwc/10))

    def iwc_variance(self, h: np.array, ice_ind: np.array) -> np.array:
        u, v = self._model_obj._set_variables('uwind', 'vwind')
        u, v = self.remove_extra_levels(u, v)
        w_shear = self.calculate_wind_shear(self._model_obj.wind, u, v, h)
        variance_iwc = self.calculate_variance_iwc(w_shear, ice_ind)
        return variance_iwc

    def calculate_variance_iwc(self, w_shear: np.array, ice_ind: np.array) -> float:
        return 10**(0.3*np.log10(self._model_obj.resolution_h) - 0.04*w_shear[ice_ind] - 1.03)

    @staticmethod
    def calculate_wind_shear(wind, u: np.array, v: np.array, height: np.array) -> np.array:
        grand_winds = []
        for w in (wind, u, v):
            grad_w = np.zeros(w.shape)
            grad_w[0, :] = (w[1, :] - w[0, :]) / (height[1, :] - height[0, :])
            grad_w[1:-2, :] = (w[2:-1, :] - 2*w[1:-2, :] + w[1:-2, :]) / \
                              (height[2:-1, :] - height[1:-2, :])
            grad_w[-1, :] = (w[-1, :] - w[-2, :]) / (height[-1, :] - height[-2, :])
            grand_winds.append(grad_w)

        w_shear = np.sqrt(np.power(grand_winds[1], 2) + np.power(grand_winds[-1], 2))
        w_shear[grand_winds[0] < 0] = 0 - w_shear[grand_winds[0] < 0]
        return w_shear

    @staticmethod
    def calculate_iwc_distribution(cloud_iwc: float, f_variance_iwc: float,
                                   n_std: int = 5, n_dist: int = 250) -> np.array:
        finish = cloud_iwc + n_std*(np.sqrt(f_variance_iwc) * cloud_iwc)
        iwc_dist = np.arange(0, finish, finish/(n_dist-1))
        if cloud_iwc < iwc_dist[2]:
            finish = cloud_iwc * 10
            iwc_dist = np.arange(0, finish, finish / n_dist - 1)
        return iwc_dist

    @staticmethod
    def gamma_distribution(iwc_dist: np.array, f_variance_iwc: float, cloud_iwc: float) -> np.array:
        def calculate_gamma_dist():
            alpha = 1/f_variance_iwc
            return 1/gamma(alpha) * (alpha/cloud_iwc)**alpha * \
                       iwc_dist[i]**(alpha-1) * ma.exp(-(alpha*iwc_dist[i]/cloud_iwc))

        p_iwc = np.zeros(iwc_dist.shape)
        for i in range(len(iwc_dist)):
            p_iwc[i] = calculate_gamma_dist()
        return p_iwc

    @staticmethod
    def get_observation_index(iwc_dist: np.array, tZT: float, tT: float, tZ: float,
                              t: float, temperature: float, z_sen: float) -> np.array:
        def calculate_min_iwc():
            min_iwc = 10**(tZT*z_sen*temperature + tT*temperature + tZ*z_sen + t)
            return min_iwc

        iwc_min = calculate_min_iwc()
        obs_index = iwc_dist > iwc_min
        return obs_index

    @staticmethod
    def filter_cirrus(p_iwc: np.array, obs_index: np.array, cf_filtered: np.array) -> np.array:
        return (np.sum(p_iwc*obs_index)/np.sum(p_iwc))*cf_filtered
