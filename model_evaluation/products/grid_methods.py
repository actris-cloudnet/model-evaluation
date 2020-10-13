import numpy as np
from model_evaluation.products import tools as tl
from cloudnetpy import utils


class CfGrid:

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
        self.time_adv = tl.calculate_advection_time(model_obj.resolution_h, model_obj.wind)
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
        self.time_steps = tl.time2datetime(time_steps, self.date)
        self._regrid_cf()
        self._regrid_cf_advection()

    def _regrid_cf(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        array_A = np.zeros(self.model_height.shape)

        for i in range(len(self.time_steps) - 1):
            x_ind = (self.time_steps[i] <= self.obs_time) &\
                    (self.obs_time < self.time_steps[i+1])
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
                array_A[i, j] = np.mean(np.sum(self.obs_data[ind], 1) > 0)

        self.model_obj.append_data(array_V, f"{self.obs}_V_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_A, f"{self.obs}_A_{self.model}{self.model_obj._cycle}")

    def _regrid_cf_advection(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        array_A = np.zeros(self.model_height.shape)

        for i in range(len(self.time_steps) - 1):
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind = ((self.model_time[i] - self.time_adv[i, j] / 2) <= self.obs_time) & \
                        (self.obs_time < (self.model_time[i+1] - self.time_adv[i+1, j] / 2))
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
                array_A[i, j] = np.mean(np.sum(self.obs_data[ind], 1) > 0)

        self.model_obj.append_data(array_V, f"{self.obs}_V_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_A, f"{self.obs}_A_adv_{self.model}{self.model_obj._cycle}")


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
        self.time_adv = tl.calculate_advection_time(model_obj.resolution_h, model_obj.wind)
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
        self.time_steps = tl.time2datetime(time_steps, self.date)
        self._regrid_data()
        self._regrid_data_advection()

    def _regrid_data(self):
        """
        Regrid thicker array to thinner one
        """
        array_iwc = np.zeros(self.model_height.shape)
        array_iwc_inc = np.zeros(self.model_height.shape)
        array_iwc_rain = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            x_ind_iwc = (self.time_steps[i] <= self.obs_time) &\
                    (self.obs_time < self.time_steps[i+1])
            x_ind_inc = (self.time_steps[i] <= self.obs_time) &\
                    (self.obs_time < self.time_steps[i+1] & ~self.obs_obj['iwc_inc_att'][:])
            x_ind_rain = (self.time_steps[i] <= self.obs_time) &\
                    (self.obs_time < self.time_steps[i+1] & ~self.obs_obj['iwc_rain'][:])
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                iwc_ind = np.outer(x_ind_iwc, y_ind)
                iwc_inc = np.outer(x_ind_inc, y_ind)
                iwc_rain = np.outer(x_ind_rain, y_ind)
                array_iwc[i, j] = np.mean(self.obs_data[iwc_ind])
                array_iwc_inc[i, j] = np.mean(self.obs_data[iwc_inc])
                array_iwc_rain[i, j] = np.mean(self.obs_data[iwc_rain])

        self.model_obj.append_data(array_iwc, f"{self.obs}_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_inc, f"{self.obs}_inc_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_rain, f"{self.obs}_rain_{self.model}{self.model_obj._cycle}")

    def _regrid_data_advection(self):
        """
        Regrid thicker array to thinner one
        """
        array_iwc = np.zeros(self.model_height.shape)
        array_iwc_inc = np.zeros(self.model_height.shape)
        array_iwc_rain = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind_iwc = ((self.model_time[i] - self.time_adv[i, j] / 2) <= self.obs_time) & \
                        (self.obs_time < (self.model_time[i+1] - self.time_adv[i+1, j] / 2))
                x_ind_inc = ((self.model_time[i] - self.time_adv[i, j] / 2) <= self.obs_time) & \
                            (self.obs_time < (self.model_time[i + 1] - self.time_adv[i + 1, j] / 2) &
                            ~self.obs_obj['iwc_inc_att'][:])
                x_ind_rain = ((self.model_time[i] - self.time_adv[i, j] / 2) <= self.obs_time) & \
                            (self.obs_time < (self.model_time[i + 1] - self.time_adv[i + 1, j] / 2) &
                            ~self.obs_obj['iwc_rain'][:])
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                iwc_ind = np.outer(x_ind_iwc, y_ind)
                iwc_inc = np.outer(x_ind_inc, y_ind)
                iwc_rain = np.outer(x_ind_rain, y_ind)
                array_iwc[i, j] = np.mean(self.obs_data[iwc_ind])
                array_iwc_inc[i, j] = np.mean(self.obs_data[iwc_inc])
                array_iwc_rain[i, j] = np.mean(self.obs_data[iwc_rain])

        self.model_obj.append_data(array_iwc, f"{self.obs}_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_inc, f"{self.obs}_inc_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_rain, f"{self.obs}_rain_adv_{self.model}{self.model_obj._cycle}")


class LwcGrid:

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
        self.time_adv = tl.calculate_advection_time(model_obj.resolution_h, model_obj.wind)
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
        self.time_steps = tl.time2datetime(time_steps, self.date)
        self._regrid_data()
        self._regrid_data_advection()

    def _regrid_data(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            x_ind = (self.time_steps[i] <= self.obs_time) &\
                    (self.obs_time < self.time_steps[i+1])
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
        self.model_obj.append_data(array_V, f"{self.obs}_{self.model}{self.model_obj._cycle}")

    def _regrid_data_advection(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind = ((self.model_time[i] - self.time_adv[i, j] / 2) <= self.obs_time) & \
                        (self.obs_time < (self.model_time[i+1] - self.time_adv[i+1, j] / 2))
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
        self.model_obj.append_data(array_V, f"{self.obs}_adv_{self.model}{self.model_obj._cycle}")

