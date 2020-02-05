import numpy as np
import numpy.ma as ma
import uuid
import datetime
from scipy import stats
from scipy.interpolate import RectBivariateSpline


SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400


def seconds2hours(time_in_seconds):
    """Converts seconds since some epoch to fraction hour.

    Args:
        time_in_seconds (ndarray): 1-D array of seconds since some epoch
            that starts on midnight.

    Returns:
        ndarray: Time as fraction hour.

    Notes:
        Excludes leap seconds.

    """
    seconds_since_midnight = np.mod(time_in_seconds, SECONDS_PER_DAY)
    fraction_hour = seconds_since_midnight/SECONDS_PER_HOUR
    if fraction_hour[-1] == 0:
        fraction_hour[-1] = 24
    return fraction_hour


def get_uuid():
    """Returns unique identifier."""
    return uuid.uuid4().hex


def isscalar(array):
    """Tests if input is scalar.

    By "scalar" we mean that array has a single value.

    Examples:
        >>> isscalar(1)
            True
        >>> isscalar([1])
            True
        >>> isscalar(np.array(1))
            True
        >>> isscalar(np.array([1]))
            True

    """
    arr = ma.array(array)
    if not hasattr(arr, '__len__') or arr.shape == () or len(arr) == 1:
        return True
    return False


def get_time():
    """Returns current UTC-time."""
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def get_source(data_handler):
    """Returns uuid (or filename if uuid not found) of the source file.

    Args:
        data_handler (netCDF Dataset): The netCDF Dataset instance.

    Returns:
        str: The `file_uuid` attribute, if exits. If missing, return the
        `filename` attribute.

    """
    return getattr(data_handler.dataset, 'file_uuid', data_handler.filename)


def lin2db(x, scale=10):
    """Linear to dB conversion."""
    return scale*ma.log10(x)


def db2lin(x, scale=10):
    """dB to linear conversion."""
    return 10**(x/scale)


def binvec(x):
    """Converts 1-D center points to bins with even spacing.

    Args:
        x (array_like): 1-D array of N real values.

    Returns:
        ndarray: N + 1 edge values.

    Examples:
        >>> binvec([1, 2, 3])
            [0.5, 1.5, 2.5, 3.5]

    """
    edge1 = x[0] - (x[1]-x[0])/2
    edge2 = x[-1] + (x[-1]-x[-2])/2
    return np.linspace(edge1, edge2, len(x)+1)


def rebin_2d(x_in, data, x_new, statistic='mean', n_min=1):
    """Rebins 2-D data in one dimension.

    Args:
        x_in (ndarray): 1-D array with shape (n,).
        data (MaskedArray): 2-D input data with shape (n, m).
        x_new (ndarray): 1-D target vector (center points)
            with shape (N,).
        statistic (str, optional): Statistic to be calculated. Possible
            statistics are 'mean', 'std'. Default is 'mean'.
        n_min (int): Minimum number of points to have good statistics in a bin.
            Default is 1.

    Returns:
        MaskedArray: Rebinned data with shape (N, m).

    Notes: 0-values are masked in the returned array.

    """
    edges = binvec(x_new)
    datai = np.zeros((len(x_new), data.shape[1]))
    data = ma.masked_invalid(data)  # data may contain nan-values
    for ind, values in enumerate(data.T):
        mask = ~values.mask
        if ma.any(values[mask]):
            datai[:, ind], _, bin_no = stats.binned_statistic(x_in[mask],
                                                              values[mask],
                                                              statistic=statistic,
                                                              bins=edges)
            if n_min > 1:
                unique, counts = np.unique(bin_no, return_counts=True)
                datai[unique[counts < n_min]-1, ind] = 0

    datai[~np.isfinite(datai)] = 0
    return ma.masked_equal(datai, 0)


def rebin_1d(x_in, data, x_new, statistic='mean'):
    """Rebins 1D array.

    Args:
        x_in (ndarray): 1-D array with shape (n,).
        data (MaskedArray): 1-D input data with shape (m,).
        x_new (ndarray): 1-D target vector (center points) with shape (N,).
        statistic (str, optional): Statistic to be calculated. Possible
            statistics are 'mean', 'std'. Default is 'mean'.

    Returns:
        MaskedArray: Rebinned data with shape (N,).

    """
    edges = binvec(x_new)
    datai = np.zeros(len(x_new))
    data = ma.masked_invalid(data)  # data may contain nan-values
    mask = ~data.mask  # pylint: disable=E1101
    if ma.any(data[mask]):
        datai, _, _ = stats.binned_statistic(x_in[mask],
                                             data[mask],
                                             statistic=statistic,
                                             bins=edges)
    datai[~np.isfinite(datai)] = 0
    return ma.masked_equal(datai, 0)


def interpolate_2d(x, y, z, x_new, y_new):
    """Linear interpolation of gridded 2d data.

    Args:
        x (ndarray): 1-D array.
        y (ndarray): 1-D array.
        z (ndarray): 2-D array at points (x, y).
        x_new (ndarray): 1-D array.
        y_new (ndarray): 1-D array.

    Returns:
        ndarray: Interpolated data.

    Notes:
        Does not work with nans. Ignores mask of masked data.
        Does not extrapolate.

    """
    fun = RectBivariateSpline(x, y, z, kx=1, ky=1)
    return fun(x_new, y_new)


def interpolate_2d_masked(array, ax_values, ax_values_new):
    """Interpolates 2D array preserving the mask.

    Args:
        array (ndarray): 2D masked array.
        ax_values (tuple): 2-element tuple containing x and y values of the input array.
        ax_values_new (tuple): 2-element tuple containing new x and y values.

    Returns:
        ndarray: Interpolated 2D masked array.

    Notes:
        Uses linear interpolation.

    """
    def _mask_invalid_values(data_in):
        data_range = (np.min(array), np.max(array))
        return ma.masked_outside(data_in, *data_range)

    data_interp = interpolate_2d(*ax_values, array, *ax_values_new)
    return _mask_invalid_values(data_interp)
