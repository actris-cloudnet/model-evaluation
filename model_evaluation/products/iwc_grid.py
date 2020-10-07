import numpy as np
from datetime import timedelta
from cloudnetpy import utils


class IwcGrid:

    def __init__(self, model_obj, obs_obj, model, obs):
        self.obs_obj = obs_obj
        self.obs = obs
        self.date = obs_obj.date
        self.obs_time = obs_obj.time
        self.obs_height = obs_obj.data['height'][:]
        self.obs_data = obs_obj.data[obs][:]
        self.model_obj = model_obj
        self.model = model
        self.model_time = model_obj.time
        self.model_height = model_obj.data[model_obj.keys['height']][:]
        self.model_reso = model_obj.resolution_h
        self.model_wind = model_obj.wind
        self.regrid_array()

    def regrid_array(self):
        """Rebins `data` in time and optionally interpolates in height.
        Args:
            old_obj (ObservationManager object): 2D data of thicker resolution Object
            new_obj (ModelGrid object): 2D data of wider resolution Object
            model (str): Name of used model
            obs (str): Name of generating observation
        """
        time_steps = utils.binvec(self.model_time)
        self.time_steps = self.time2datetime(time_steps, self.date)

        volume_grid, area_grid = self.regrid_data()
        self.model_obj.append_data(volume_grid, f"{self.obs}_V_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(area_grid, f"{self.obs}_A_{self.model}{self.model_obj._cycle}")

        volume_adv_grid, area_adv_grid = self.regrid_data_advection()
        self.model_obj.append_data(volume_adv_grid, f"{self.obs}_V_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(area_adv_grid, f"{self.obs}_A_adv_{self.model}{self.model_obj._cycle}")

    def _regrid_data(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            x_ind = (self.time_steps[i] <= self.obs_time) &\
                    (self.obs_time < self.time_steps[i+1])
            y_steps = self.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
        return array_V

    def _regrid_data_advection(self):
        """
        Regrid thicker array to thinner one
        """
        t_adv = self.calculate_advection_time()
        array_V = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            y_steps = self.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind = ((self.model_time[i] - t_adv[i, j] / 2) <= self.obs_time) & \
                        (self.obs_time < (self.model_time[i+1] - t_adv[i+1, j] / 2))
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
        return array_V

    def time2datetime(self, time_arr, date):
        return np.asarray([date + timedelta(hours=float(time)) for time in time_arr])

    def rebin_edges(self, arr):
        """Rebins array bins by half and adds boundaries."""
        new_arr = [(arr[i] + arr[i+1])/2 for i in range(len(arr)-1)]
        new_arr.insert(0, arr[0] - ((arr[0] + arr[1])/2))
        new_arr.insert(len(new_arr), arr[-1] + (arr[-1] - arr[-2]))
        return np.array(new_arr)

    def add_date(self):
        for a in ('year', 'month', 'day'):
            self.model_obj.date.append(getattr(self.obs_obj.dataset, a))

    def calculate_advection_time(self):
        return ((self.model_reso * 1000) / self.model_wind) / 60**2

