import numpy as np
import numpy.ma as ma
from datetime import timedelta


def time2datetime(time_arr, date):
    return np.asarray([date + timedelta(hours=float(time)) for time in time_arr])


def rebin_edges(arr):
    """Rebins array bins by half and adds boundaries."""
    new_arr = [(arr[i] + arr[i + 1]) / 2 for i in range(len(arr) - 1)]
    new_arr.insert(0, arr[0] - ((arr[0] + arr[1]) / 2))
    new_arr.insert(len(new_arr), arr[-1] + (arr[-1] - arr[-2]))
    return np.array(new_arr)


def calculate_advection_time(resolution, wind, sampling):
    """Calculates time which variable take to cross through time window

        Notes:
            Wind speed is higher in upper levels, so advection time is more
            there then lower levels. Effect is small in a mid-latitudes,
            but visible in a tropics.

            sampling = 1 -> hour, sampling 1/6 -> 10min

        References:
    """
    t_adv = resolution.data * 1000 / wind / 60 ** 2
    t_adv[t_adv > 1/sampling] = 1/sampling
    return np.asarray([[timedelta(hours=float(t)) for t in time] for time in t_adv])


def get_1d_indices(window, data, mask=None):
    if mask is not None:
        data = ma.array(data)
        data[mask] = ma.masked
    indices = (window[0] <= data) & (data < window[-1])
    return indices


def get_adv_indices(model_t, adv_t, data, mask=None):
    if mask is not None:
        data = ma.array(data)
        data[mask] = ma.masked
    adv_indices = ((model_t - adv_t / 2) <= data) & (data < (model_t + adv_t / 2))
    return adv_indices


def get_obs_window_size(ind_x, ind_y):
    """Returns shape (tuple) of window area, where values are True"""
    x = np.where(ind_x)[0]
    y = np.where(ind_y)[0]
    if np.any(x) and np.any(y):
        return x[-1] - x[0] + 1, y[-1] - y[0] + 1
    return None


def add_date(model_obj, obs_obj):
    for a in ('year', 'month', 'day'):
        model_obj.date.append(getattr(obs_obj.dataset, a))


def average_column_sum(data):
    """Returns average sum of columns which have any data"""
    return np.nanmean(np.nansum(data, 1) > 0)
