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
from scipy import stats
from cloudnetpy import utils
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
        data (ndarray): 2D data of thicker resolution array
        time (ndarray): 1D time array ow thicker resolution.
        time_new (ndarray): 1D time array wider resolution.
        height (ndarray): 1D height array of thicker resolution.
        height_new (ndarray): 2D height array wider resolution
    """
    time_steps = utils.binvec(time_new)
    for i, t in enumerate(time_steps):
        time_values = np.where(t <= time > t)
        height_steps = utils.binvec(height_new[i])




    return data

