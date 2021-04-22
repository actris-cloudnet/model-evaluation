import sys
import os
import numpy as np
import numpy.ma as ma
from typing import Tuple

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DayStatistics:
    def __init__(self, method: str,
                 product_into: list,
                 model: np.array,
                 observation: np.array):
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
        self.model_array = model
        self.obs_array = observation
        self._generate_day_statistics()

    def _get_method_attr(self):
        full_name = ""
        if self.method == 'error':
            full_name = 'relative_error'
        if self.method == 'aerror':
            full_name = 'absolute_error'
        if self.method == 'area':
            full_name = 'calc_common_area_sum'
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


def relative_error(product: list, model: ma.array, observation: ma.array) -> Tuple:
    model, observation = combine_masked_indices(model, observation)
    error = ((model - observation) / observation) * 100
    title = f"{product[1]} vs {product[-1]}"
    return np.round(error, 2), title


def absolute_error(product: list, model: ma.array, observation: ma.array) -> Tuple:
    model, observation = combine_masked_indices(model, observation)
    error = (observation - model) * 100
    title = f"{product[1]} vs {product[-1]}"
    return np.round(error, 2), title


def combine_masked_indices(model: ma.array, observation: ma.array):
    """ Connects two array masked indices to one and add in two array same mask """
    observation[np.where(np.isnan(observation))] = ma.masked
    model[model < np.min(observation)] = ma.masked
    combine_mask = model.mask + observation.mask
    model[combine_mask] = ma.masked
    observation[combine_mask] = ma.masked
    return model, observation


def calc_common_area_sum(product: list, model: ma.array, observation: ma.array) -> Tuple:
    def _indices_of_mask_sum():
        # Calculate percentage value of common area of indices from two arrays.
        # Results is total number of common indices with value
        observation[np.where(np.isnan(observation))] = ma.masked
        model[np.where(np.isnan(model))] = ma.masked
        model[model < np.min(observation)] = ma.masked
        combine_mask = model.mask + observation.mask
        common_mask = np.bitwise_and(model.mask == True, observation.mask == True)
        match = np.sum(~combine_mask) / np.sum(~common_mask) * 100
        return np.round(match, 2)
    match = _indices_of_mask_sum()
    title = f"{product[1]} vs {product[-1]}"
    return match, title


def histogram(product: list, model: ma.array, observation: ma.array) -> Tuple:
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


def vertical_profile(product: list, model: ma.array, observation: ma.array) -> Tuple:
    if model.shape[0] > 25:
        model = model.T
        observation = observation.T
    model_vertical = ma.mean(model, axis=0)
    obs_vertical = np.nanmean(observation, axis=0)
    title = f"{product[-1]}"
    return (model_vertical, obs_vertical), (title, product[1])
