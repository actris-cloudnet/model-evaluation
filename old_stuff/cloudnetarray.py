import numpy as np
import numpy.ma as ma
from old_stuff import utils


class CloudnetArray:
    """Stores netCDF4 variables as CloudnetArrays.

    Args:
        netcdf4_variable (netCDF4 Variable): The netCDF4 :class:`Variable` instance.
        name (str): Name of the variable.
        units_from_user (str, optional): Units of the variable.

    Attributes:
        name (str): Name of the variable.
        data (array_like): The actual data.
        data_type (str): 'i4' for integers, 'f4' for floats.
        units (str): The `units_from_user` argument if it is given. Otherwise
            copied from the original netcdf4 variable.

    """

    def __init__(self, netcdf4_variable, name, units_from_user=None):
        self.name = name
        self.data = self._get_data(netcdf4_variable)
        self.data_type = self._init_data_type()
        self.units = self._init_units(units_from_user, netcdf4_variable)

    def __getitem__(self, ind):
        return self.data[ind]

    @staticmethod
    def _get_data(array):
        return array if utils.isscalar(array) else array[:]

    @staticmethod
    def _init_units(units_from_user, netcdf4_variable):
        if units_from_user:
            return units_from_user
        return getattr(netcdf4_variable, 'units', '')

    def _init_data_type(self):
        if ((isinstance(self.data, np.ndarray) and self.data.dtype
             in (np.float32, np.float64)) or isinstance(self.data, float)):
            return 'f4'
        return 'i4'

    def mask_indices(self, ind):
        """Masks data from given indices.

        Args:
            ind (tuple): Indices to be masked.

        """
        self.data[ind] = ma.masked

    def rebin_data(self, time, time_new, height=None, height_new=None):
        """Rebins `data` in time and optionally interpolates in height.

        Args:
            time (ndarray): 1D time array.
            time_new (ndarray): 1D new time array.
            height (ndarray, optional): 1D height array.
            height_new (ndarray, optional): 1D new height array. Should be
                given if also `height` is given.

        """
        if self.data.ndim == 1:
            self._rebin_1d_data(time, time_new)
        else:
            self.data = utils.rebin_2d(time, self.data, time_new)
            if np.any(height) and np.any(height_new):
                self.data = utils.interpolate_2d_masked(self.data,
                                                        (time_new, height),
                                                        (time_new, height_new))

    def _rebin_1d_data(self, time, time_new):
        """Rebins 1D array in time."""
        self.data = utils.rebin_1d(time, self.data.astype(float), time_new)

    def fetch_attributes(self):
        """Returns list of user-defined attributes."""
        for attr in self.__dict__:
            if attr not in ('name', 'data', 'data_type'):
                yield attr

    def set_attributes(self, attributes):
        """Set some attributes if they exist.

        Args:
            attributes (MetaData): The :class:`MetaData` instance, containing
                name / value pairs to be added as instance attributes.

        """
        for key in attributes._fields:  # To iterate namedtuple fields.
            data = getattr(attributes, key)
            if data:
                setattr(self, key, data)
