"""
Gets: product from level 2a/cat-file and model witch will be used for griding.

Model file at this point is probably including only one grid point witch represents
the sites location. Selecting correct grid point will be chosen in other file. Depend on
the state of model files.

This is moved to later state.
"""
import os
import sys
import numpy as np
import netCDF4
import configparser


def generate_data2modelgrid(cnet_file, model_file, quantity=None):
    """

    Args:
        cnet_file (str): Path to cloudnet product file
        model_file (str): Path to model file
        quantity (str) (Optional): Select quantity in cnet_file

    Returns:

    """
    print("lol")
    "Tähän perus gridauksen prosessointi"

# def rebin_data(self, time, time_new, height=None, height_new=None):
#        """Rebins `data` in time and optionally interpolates in height.
#        Args:
#            time (ndarray): 1D time array.
#            time_new (ndarray): 1D new time array.
#            height (ndarray, optional): 1D height array.
#            height_new (ndarray, optional): 1D new height array. Should be
#                given if also `height` is given.
#        """
#        if self.data.ndim == 1:
#            self._rebin_1d_data(time, time_new)
#        else:
#            self.data = utils.rebin_2d(time, self.data, time_new)
#            if np.any(height) and np.any(height_new):
#                self.data = utils.interpolate_2d_masked(self.data,
#                                                        (time_new, height),
#                                                        (time_new, height_new))


# def _rebin_1d_data(self, time, time_new):
#    """Rebins 1D array in time."""
#    self.data = utils.rebin_1d(time, self.data.astype(float), time_new)


