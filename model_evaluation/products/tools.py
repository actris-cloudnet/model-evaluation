import numpy as np
from datetime import timedelta


def time2datetime(time_arr, date):
    return np.asarray([date + timedelta(hours=float(time)) for time in time_arr])


def rebin_edges(arr):
    """Rebins array bins by half and adds boundaries."""
    new_arr = [(arr[i] + arr[i + 1]) / 2 for i in range(len(arr) - 1)]
    new_arr.insert(0, arr[0] - ((arr[0] + arr[1]) / 2))
    new_arr.insert(len(new_arr), arr[-1] + (arr[-1] - arr[-2]))
    return np.array(new_arr)


def calculate_advection_time(resolution, wind):
    t_adv = ((resolution.data * 1000) / wind) / 60 ** 2
    return np.asarray([[timedelta(seconds=float(t)) for t in time] for time in t_adv])


def get_1d_indices(ind, x_window, data, mask=False):
    if mask is True: # TODO: Miksi toimii näin, muttei if mask?
        data = data[mask]
    x_indices = (x_window[ind] <= data) & (data < x_window[ind + 1])
    return x_indices


def get_adv_indices(i, j, model_t, adv_t, data, mask=False):
    if mask is True: #TODO: ei pelitä vielä kunnolla
        data = data[mask]
    adv_indices = ((model_t[i] + adv_t[i, j]/2) <= data) & \
                  (data < (model_t[i] - adv_t[i, j]/2))
    return adv_indices


def get_obs_window_size(ind_x, ind_y):
    x = np.where(ind_x == True)[0]
    y = np.where(ind_y == True)[0]
    return x[-1] - x[0] + 1, y[-1] - y[0] + 1
