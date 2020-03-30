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
from datetime import datetime, timedelta
from scipy import stats
from cloudnetpy import utils
from cloudnetpy.categorize.datasource import DataSource
from model_evaluation.products.regrid_observation import ModelGrid
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.metadata import L3_ATTRIBUTES
from model_evaluation.products.cloud_fraction import generate_cv


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
    product_obj = ObservationManager(obs, product_file)
    for m_file in model_files:
        data_obj = ModelGrid(m_file, model, output_file, obs)
        data_obj = regrid_array(product_obj, data_obj, model, obs)
        update_attributes(data_obj.data, L3_ATTRIBUTES)

        if os.path.isfile(output_file) is False:
            save_modelfile(f"{model}_products", data_obj, model_files, output_file)
        else:
            add_var2ncfile(data_obj, output_file)


def regrid_array(old_obj, new_obj, model, obs):
    """Rebins `data` in time and optionally interpolates in height.
    Args:
        old_obj (ObservationManager object): 2D data of thicker resolution Object
        new_obj (ModelGrid object): 2D data of wider resolution Object
        model (str): Name of used model
        obs (str): Name of generating observation
    """
    regrid_array = np.zeros(new_obj.data[new_obj.keys[obs]][:].shape)

    time_steps = utils.binvec(new_obj.time)
    time_steps = time2datetime(time_steps, old_obj.date)
    old_time = time2datetime(old_obj.time, old_obj.date)

    for i in range(len(time_steps) - 1):
        time_index = (old_time >= time_steps[i]) & (old_time < time_steps[i+1])
        height_steps = utils.binvec(new_obj.data[new_obj.keys['height']][:][i])

        for j in range(len(height_steps)-1):
            height_index = (old_obj.data['height'][:] >= height_steps[j]) & \
                           (old_obj.data['height'][:] < height_steps[j+1])
            index = np.outer(time_index, height_index)
            regrid_array[i, j] = np.mean(old_obj.data[obs][:][index])
    new_obj.append_data(regrid_array, f"{obs}_obs_{model}{new_obj._cycle}")
    return new_obj


def time2datetime(time_array, date):
    return np.asarray([date + timedelta(hours=float(time)) for time in time_array])


class ObservationManager(DataSource):
    """This class will read and generate observation to wanted format"""
    def __init__(self, obs, obs_file):
        super().__init__(obs_file)
        self.obs = obs
        self.file = obs_file
        self.date = self._get_date()
        self._generate_product()

    def _generate_product(self):
        if self.obs is 'cv':
            print("")
            # Generate needed information for calculating cloud fraction
            # Kutsutaan Cloud fraction luokkaa hoitamaan homma
            # Palauttaa datan halutussa muodossa, jotta voidaan tehdä gridaaminen
            self.data = generate_cv(self.data, self.file)
        else:
            self.append_data(self.getvar(self.obs), self.obs)
        self.append_data(self.getvar('height'), 'height')

    def _get_date(self):
        """Returns measurement date string."""
        nc = netCDF4.Dataset(self.file)
        case_date = datetime(int(nc.year), int(nc.month), int(nc.day), 0, 0, 0)
        nc.close()
        return case_date




#TODO: Think if possible to do
#data = [[np.mean(data[np.where(t <= time > t), np.where(h >= height > h)])
#         for h in utils.binvec(height_new[i])]
#        for i, t in enumerate(utils.binvec(time_new))]