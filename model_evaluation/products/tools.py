import numpy as np
import numpy.ma as ma
import datetime
import logging
from typing import Union
from datetime import timedelta
from model_evaluation.products.model_products import ModelManager
from model_evaluation.products.observation_products import ObservationManager


def check_model_file_list(name: str, models: list):
    """Check that files in models are from same model and date"""
    for m in models:
        if name not in m:
            logging.error(f'Invalid model file set')
            raise AttributeError(f'{m} not from {name}')


def time2datetime(time: np.array, date: datetime.datetime):
    return np.asarray([date + timedelta(hours=float(t)) for t in time])


def rebin_edges(arr: np.array):
    """Rebins array bins by half and adds boundaries."""
    new_arr = [(arr[i] + arr[i + 1]) / 2 for i in range(len(arr) - 1)]
    new_arr.insert(0, arr[0] - ((arr[0] + arr[1]) / 2))
    new_arr.insert(len(new_arr), arr[-1] + (arr[-1] - arr[-2]))
    return np.array(new_arr)


def calculate_advection_time(resolution: int, wind: np.array, sampling: int):
    """Calculates time which variable takes to go through the time window

        Notes:
            Wind speed is stronger in upper levels, so advection time is more
            there then lower levels. Effect is small in a mid-latitudes,
            but visible in a tropics.

            sampling = 1 -> hour, sampling 1/6 -> 10min

        References:
    """
    t_adv = resolution * 1000 / wind / 60 ** 2
    t_adv[t_adv.mask] = 0
    t_adv[t_adv > 1/sampling] = 1/sampling
    return np.asarray([[timedelta(hours=float(t)) for t in time] for time in t_adv])


def get_1d_indices(window: tuple, data: np.array, mask: np.array = None):
    indices = (window[0] <= data) & (data < window[-1])
    if mask is not None:
        indices[mask] = ma.masked
    return indices


def get_adv_indices(model_t: int, adv_t: float, data: np.array, mask: np.array = None):
    adv_indices = ((model_t - adv_t / 2) <= data) & (data < (model_t + adv_t / 2))
    if mask is not None:
        adv_indices[mask] = ma.masked
    return adv_indices


def get_obs_window_size(ind_x: np.array, ind_y: np.array) -> Union[tuple, None]:
    """Returns shape (tuple) of window area, where values are True"""
    x = np.where(ind_x)[0]
    y = np.where(ind_y)[0]
    if np.any(x) and np.any(y):
        return x[-1] - x[0] + 1, y[-1] - y[0] + 1
    return None


def add_date(model_obj: ModelManager, obs_obj: ObservationManager):
    for a in ('year', 'month', 'day'):
        model_obj.date.append(getattr(obs_obj.dataset, a))


def average_column_sum(data: np.array):
    """Returns average sum of columns which have any data"""
    return np.nanmean(np.nansum(data, 1) > 0)
