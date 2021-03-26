import sys
import os
import numpy as np
import numpy.ma as ma
import cloudnetpy.utils as utils

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DayStatistics:
    def __init__(self, method, product_into, model_array, obs_array):
        """ Class for calculating statistical analysis of day scale products

        Class generates one statistical method at the time with given model data
        and observation data of wanted product.

        Args:
            method (str): Name on statistical method to be calculated
            product_into (list): List of information of statistical ananlysis is
                                 done with. A list includes observed product name (str),
                                 model variable (str) name and observation variable name (str)
            model_array (MaskedArray): Ndarray of product model simulation
            obs_array (MaskedArray): Ndarray of product resampled observation

        Raises:
            RuntimeError: Not found function by given method

        Returns:
            day_statistic (object): The :class:'DayStatistic' object.

        Examples:
            >>> from model_evaluation.products.product_resampling import process_observation_resample2model
            >>> method = 'error'
            >>> product_info = ['cf', 'European Centre for Medium-Range Weather Forecasts', 'ecmwf']
            >>> model_array = np.array([[1,1,1],[1,1,1],[1,1,1]])
            >>> obs_array = np.array([[1,1,1],[1,1,1],[1,1,1]])
            >>> day_stat = DayStatistics(method, product_into, model_array, obs_array)
        """
        self.method = method
        self.product = product_into
        self.model_array = model_array
        self.obs_array = obs_array
        self._generate_day_statistics()

    def _get_method_attr(self):
        full_name = ""
        if self.method == 'error':
            full_name = 'relative_error'
        if self.method == 'aerror':
            full_name = 'absolute_error'
        if self.method == 'cov':
            full_name = 'calc_common_ind_sum'
        if self.method == 'hist':
            full_name = 'histogram'
        if self.method == 'vertical':
            full_name = 'vertical_profile'
        params = (self.product, self.model_array, self.obs_array)
        return full_name, params

    def _generate_day_statistics(self):
        full_name, params = self._get_method_attr()
        cls = __import__("statistical_methods")
        try:
            self.stat_data, self.title = getattr(cls, f"{full_name}")(*params)
        except RuntimeError as error:
            print(error)


def relative_error(product, model, observation):
    model, observation = combine_mask_indices(model, observation)
    error = ((model - observation) / observation) * 100
    title = f"{product[1]} vs {product[-1]}"
    return np.round(error, 2), title


def absolute_error(product, model, observation):
    model, observation = combine_mask_indices(model, observation)
    error = (observation - model) * 100
    title = f"{product[1]} vs {product[-1]}"
    return np.round(error, 2), title


def combine_mask_indices(model, observation):
    """ Connects two array masked indices to one and add in two array same mask """
    observation[np.where(np.isnan(observation))] = ma.masked
    unity_mask = model.mask + observation.mask
    model[unity_mask] = ma.masked
    observation[unity_mask] = ma.masked
    return model, observation


def calc_common_ind_sum(product, model, observation):
    def _indices_of_mask_sum():
        # Calculate percentage value of common value indices of two array from
        # total number of value indices
        observation[np.where(np.isnan(observation))] = ma.masked
        unity_mask = model.mask + observation.mask
        total_mask = np.bitwise_and(model.mask == True, observation.mask == True)
        match = sum(sum(~unity_mask)) / sum(sum(~total_mask)) * 100
        return np.round(match, 2)
    match = _indices_of_mask_sum()
    title = f"{product[1]} vs {product[-1]}"
    return match, title


def histogram(product, model, observation):
    if 'cf' in product:
        model = ma.round(model[~model.mask].data, decimals=1).flatten()
        observation = ma.round(observation[~observation.mask].data,
                               decimals=1).flatten()
    else:
        model = ma.round(model[~model.mask].data, decimals=6).flatten()
        observation = ma.round(observation[~observation.mask].data,
                               decimals=6).flatten()
    observation = observation[~np.isnan(observation)]
    hist_bins = np.histogram(observation, density=True)[-1]
    model[model > hist_bins[-1]] = hist_bins[-1]
    title = f"{product[-1]}"
    return ((model, hist_bins), (observation, hist_bins)), (title, product[1])


def vertical_profile(product, model, observation):
    model_vertical = ma.mean(model, axis=0)
    obs_vertical = np.nanmean(observation, axis=0)
    title = f"{product[-1]}"
    return (model_vertical, obs_vertical), (title, product[1])

