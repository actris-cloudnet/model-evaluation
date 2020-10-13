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
    return ((resolution * 1000) / wind) / 60 ** 2

