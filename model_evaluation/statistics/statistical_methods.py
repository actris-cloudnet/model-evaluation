import sys
import os
import numpy as np
import numpy.ma as ma
import cloudnetpy.utils as utils

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DayStatistics:
    def __init__(self, method, product, model_array, obs_array):
        """
        Class that generates statistical analysis for day scale products.
        The point is to analyze and point out the best simulation-observation
        combination. So which is the best resampled observations match with simulations?

        Args:
            product (list): A list including observed product name, model variable
                            name and observation variable name
            model_array (MaskedArray): Ndarray of product model simulation
            obs_array (MaskedArray): Ndarray of product resampled observation
        """
        self.method = method
        self.product = product
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
            full_name = 'coverage_mask'
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


class MonthStatistics:
    # TODO: Finish this at some point when needed
    # Longer time series will use file generating this way
    def __init__(self, product, data_obj):
        """
        Class that generates statistical analysis for day scale products.
        The point is to analyze and point out the best simulation-observation
        combination. So which is the best resampled observations match with simulations?

        Args:
            product (str): the name of observed product
            data_obj (object): The :class:'DataManager' object
        """
        self.product = product
        self.data_obj = data_obj
        self.model_run = data_obj.group.keys()
        self.group = data_obj.group

    def generate_day_statistics(self):
        for run in self.model_run:
            data_group = self.group[run]


def relative_error(product, model, observation):
    def unify_array_mask():
        unity_mask = model.mask + observation.mask
        model[unity_mask] = ma.masked
        observation[unity_mask] = ma.masked
        return model, observation
    model, observation = unify_array_mask()
    error = utils.calc_relative_error(model, observation)
    title = f"{product[1]} vs {product[-1]}"
    return error, title


def absolute_error(product, model, observation):
    def unify_array_mask():
        unity_mask = model.mask + observation.mask
        model[unity_mask] = ma.masked
        observation[unity_mask] = ma.masked
        return model, observation

    model, observation = unify_array_mask()
    error = (observation - model) * 100
    title = f"{product[1]} vs {product[-1]}"
    return error, title


def coverage_mask(product, model, observation):
    def _area_of_array_mask():
        observation[np.where(np.isnan(observation))] = ma.masked
        unity_mask = model.mask + observation.mask
        total_mask = np.bitwise_and(model.mask == True, observation.mask == True)
        match = sum(sum(~unity_mask)) / sum(sum(~total_mask)) * 100
        return np.round(match, 2)
    # Calculates how well two masked areas covers each other
    match = _area_of_array_mask()
    title = f"{product[1]} vs {product[-1]}"
    return match, title


def histogram(product, model, observation):
    # make histogram from all height at one
    if 'cf' in product:
        model = ma.round(model[~model.mask].data, decimals=1).flatten()
        observation = ma.round(observation[[~observation.mask]].data,
                               decimals=1).flatten()
    else:
        model = ma.round(model[~model.mask].data, decimals=6).flatten()
        observation = ma.round(observation[~observation.mask].data,
                               decimals=6).flatten()
    observation = observation[~np.isnan(observation)]
    hist_bins = np.histogram(observation, density=True)[-1]
    title = f"{product[1]} vs {product[-1]}"
    return ((model, hist_bins), (observation, hist_bins)), title


def vertical_profile():
    print("")
    # Voi olla, että tästä tulee oma luokka tai tällä on submetodeja


def verification():
    print("")


def scatter():
    print("")


def timeseries():
    print("")
    # Voi olla, että tästä tulee oma luokka tai tällä on submetodeja


def correlation():
    print("")
    # Voidaan ehkä hyödyntää vasta climatologia vaiheessa
