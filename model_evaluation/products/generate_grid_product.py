"""
This file will process observated iwc to model grid and creates the model_iwc_grid.nv file

The file will include all avaible cycles for model and regrided observation for each cycle.
Also other needed information for cycle will be saved to file.

TODO: How to get correct file path for obs?
"""
import os
import numpy as np
import configparser
import netCDF4
from cloudnetpy.utils import rebin_1d, rebin_2d, interpolate_2d_masked
from model_evaluation.products.regrid_observation import ModelGrid
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.metadata import L3_ATTRIBUTES


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


def generate_regrid_products(model, obs, model_files, output_file):
    """Read observation and regrids them to model grid.
        Creates and saves file also

        Args:
            model (str): name of model
            model_files (list): List of files from model to be generated
            obs (str): name of product to generate
            output_file (str): name of model output file
    """
    product_file = CONF['products'][obs]
    # TODO: Get observation products in here
    iwc_obs = netCDF4.Dataset(product_file).variables[obs][:]
    for m_file in model_files:
        data_obj = ModelGrid(m_file, model, output_file, obs)
        #TODO: Regrid obs to model
        update_attributes(data_obj.data, L3_ATTRIBUTES)

        if os.path.isfile(output_file) is False:
            save_modelfile(f"{model}_products", data_obj, model_files, output_file)
        else:
            add_var2ncfile(data_obj, output_file)


def rebin_data(data, time, time_new, height, height_new):
    """Rebins `data` in time and optionally interpolates in height.
    Args:
        time (ndarray): 1D time array.
        time_new (ndarray): 1D new time array.
        height (ndarray, optional): 1D height array.
        height_new (ndarray, optional): 1D new height array. Should be
            given if also `height` is given.
    """
    data = rebin_2d(time, data, time_new)
    data = interpolate_2d_masked(data, (time_new, height),
                                       (time_new, height_new))
    return data

