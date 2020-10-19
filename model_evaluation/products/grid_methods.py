import numpy as np
from model_evaluation.products import tools as tl
from cloudnetpy import utils


class CfGrid:

    def __init__(self, model_obj, obs_obj, model, obs):
        self.obs_obj = obs_obj
        self.obs = obs
        self.date = obs_obj.date
        self.obs_time = tl.time2datetime(obs_obj.time, self.date)
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
            x_ind = tl.get_1d_indices(i, self.time_steps, self.obs_time)
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = tl.get_1d_indices(j, y_steps, self.obs_height)
                ind = np.outer(x_ind, y_ind)
                if not self.obs_data[ind].any(): #TODO: parempi metodi tähän
                    array_V[i, j] = np.nan
                    array_A[i, j] = np.nan
                    continue
                window_size = tl.get_obs_window_size(x_ind, y_ind)
                data = self.obs_data[ind].reshape(window_size)
                array_V[i, j] = np.mean(data)
                array_A[i, j] = np.mean(np.sum(data, 1) > 0)
        self.model_obj.append_data(array_V, f"{self.obs}_V_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_A, f"{self.obs}_A_{self.model}{self.model_obj._cycle}")

    def _regrid_cf_advection(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        array_A = np.zeros(self.model_height.shape)
        model_t = tl.time2datetime(self.model_time, self.date)
        for i in range(len(self.time_steps) - 1):
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind = tl.get_adv_indices(i, j, model_t, self.time_adv, self.obs_time)
                y_ind = tl.get_1d_indices(j, y_steps, self.obs_height)
                ind = np.outer(x_ind, y_ind)
                if not self.obs_data[ind].any(): #TODO: parempi metodi tähän
                    array_V[i, j] = np.nan
                    array_A[i, j] = np.nan
                    continue
                window_size = tl.get_obs_window_size(x_ind, y_ind)
                data = self.obs_data[ind].reshape(window_size)

                array_V[i, j] = np.mean(data)
                array_A[i, j] = np.mean(np.sum(data, 1) > 0)

        self.model_obj.append_data(array_V, f"{self.obs}_V_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_A, f"{self.obs}_A_adv_{self.model}{self.model_obj._cycle}")


class IwcGrid:

    def __init__(self, model_obj, obs_obj, model, obs):
        self.obs_obj = obs_obj
        self.obs = obs
        self.date = obs_obj.date
        self.obs_time = tl.time2datetime(obs_obj.time, self.date)
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
        self._regrid_iwc()
        self._regrid_iwc_advection()

    def _regrid_iwc(self):
        """
        Regrid thicker array to thinner one
        """
        array_iwc = np.zeros(self.model_height.shape)
        array_iwc_mask = np.zeros(self.model_height.shape)
        array_iwc_att = np.zeros(self.model_height.shape)
        array_iwc_rain = np.zeros(self.model_height.shape)

        iwc_att = self.obs_obj.data['iwc_att'][:]
        iwc_mask = self.obs_obj.data['iwc_mask'][:]
        for i in range(len(self.time_steps) - 1):
            x_ind = tl.get_1d_indices(i, self.time_steps, self.obs_time)
            x_ind_rain = tl.get_1d_indices(i, self.time_steps, self.obs_time,
                                           mask=~self.obs_obj.data['iwc_rain'][:])
            # TODO: raining ei tod toimi
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = tl.get_1d_indices(j, y_steps, self.obs_height)
                iwc_ind = np.outer(x_ind, y_ind)
                iwc_rain_ind = np.outer(x_ind_rain, y_ind)
                array_iwc[i, j] = np.mean(self.obs_data[iwc_rain_ind])
                array_iwc_att[i, j] = np.mean(iwc_att[iwc_rain_ind])
                array_iwc_rain[i, j] = np.mean(self.obs_data[iwc_ind])
                array_iwc_mask[i, j] = np.mean(iwc_mask[iwc_rain_ind])

        self.model_obj.append_data(array_iwc, f"{self.obs}_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_mask, f"{self.obs}_mask_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_att, f"{self.obs}_att_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_rain, f"{self.obs}_rain_{self.model}{self.model_obj._cycle}")

    def _regrid_iwc_advection(self):
        """
        Regrid thicker array to thinner one
        """
        array_iwc = np.zeros(self.model_height.shape)
        array_iwc_mask = np.zeros(self.model_height.shape)
        array_iwc_att = np.zeros(self.model_height.shape)
        array_iwc_rain = np.zeros(self.model_height.shape)
        iwc_att = self.obs_obj.data['iwc_att'][:]
        iwc_mask = self.obs_obj.data['iwc_mask'][:]
        model_t = tl.time2datetime(self.model_time, self.date)
        for i in range(len(self.time_steps) - 1):
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind = tl.get_adv_indices(i, j, model_t, self.time_adv, self.obs_time)
                x_ind_rain = tl.get_adv_indices(i, j, model_t, self.time_adv,
                                                self.obs_time, mask=~self.obs_obj.data['iwc_rain'][:])
                y_ind = (y_steps[j] <= self.obs_height) & (self.obs_height < y_steps[j+1])
                iwc_ind = np.outer(x_ind, y_ind)
                iwc_rain_ind = np.outer(x_ind_rain, y_ind)
                array_iwc[i, j] = np.mean(self.obs_data[iwc_rain_ind])
                array_iwc_att[i, j] = np.mean(iwc_att[iwc_rain_ind])
                array_iwc_rain[i, j] = np.mean(self.obs_data[iwc_ind])
                array_iwc_mask[i, j] = np.mean(iwc_mask[iwc_rain_ind])

        self.model_obj.append_data(array_iwc, f"{self.obs}_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_mask, f"{self.obs}_mask_adv{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_att, f"{self.obs}_att_adv_{self.model}{self.model_obj._cycle}")
        self.model_obj.append_data(array_iwc_rain, f"{self.obs}_rain_adv_{self.model}{self.model_obj._cycle}")


class LwcGrid:

    def __init__(self, model_obj, obs_obj, model, obs):
        self.obs_obj = obs_obj
        self.obs = obs
        self.date = obs_obj.date
        self.obs_time = tl.time2datetime(obs_obj.time, self.date)
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
        self._regrid_lwc()
        self._regrid_lwc_advection()

    def _regrid_lwc(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        for i in range(len(self.time_steps) - 1):
            x_ind = tl.get_1d_indices(i, self.time_steps, self.obs_time)
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                y_ind = tl.get_1d_indices(j, y_steps, self.obs_height)
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
        self.model_obj.append_data(array_V, f"{self.obs}_{self.model}{self.model_obj._cycle}")

    def _regrid_lwc_advection(self):
        """
        Regrid thicker array to thinner one
        """
        array_V = np.zeros(self.model_height.shape)
        model_t = tl.time2datetime(self.model_time, self.date)
        for i in range(len(self.time_steps) - 1):
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps)-1):
                x_ind = tl.get_adv_indices(i, j, model_t, self.time_adv, self.obs_time)
                y_ind = tl.get_1d_indices(j, y_steps, self.obs_height)
                ind = np.outer(x_ind, y_ind)
                array_V[i, j] = np.mean(self.obs_data[ind])
        self.model_obj.append_data(array_V, f"{self.obs}_adv_{self.model}{self.model_obj._cycle}")

