import numpy as np
from model_evaluation.products import tools as tl
from cloudnetpy import utils


class ProductGrid:

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
        time_steps = utils.binvec(self.model_time)
        self.time_steps = tl.time2datetime(time_steps, self.date)
        self.grid_regeneration_product()

    def grid_regeneration_product(self):
        product_dict, product_adv_dict = self._get_method_storage()
        model_t = tl.time2datetime(self.model_time, self.date)
        for i in range(len(self.time_steps) - 1):
            x_ind = tl.get_1d_indices(i, self.time_steps, self.obs_time)
            if self.obs is 'iwc':
                x_ind_rain = tl.get_1d_indices(i, self.time_steps, self.obs_time,
                                               mask=~self.obs_obj.data['iwc_rain'][:])
            y_steps = tl.rebin_edges(self.model_height[i])
            for j in range(len(y_steps) - 1):
                x_ind_adv = tl.get_adv_indices(i, j, model_t, self.time_adv, self.obs_time)
                y_ind = tl.get_1d_indices(j, y_steps, self.obs_height)
                ind = np.outer(x_ind, y_ind)
                ind_avd = np.outer(x_ind_adv, y_ind)
                if self.obs is 'cf':
                    data = self._reshape_data_to_window(ind, x_ind, y_ind)
                    product_dict = self._regrid_cf(product_dict, i, j, data)
                    data_adv = self._reshape_data_to_window(ind_avd, x_ind_adv, y_ind)
                    product_adv_dict = self._regrid_cf(product_adv_dict, i, j, data_adv)
                elif self.obs is 'iwc':
                    x_ind_rain_adv = tl.get_adv_indices(i, j, model_t, self.time_adv, self.obs_time,
                                                        mask=~self.obs_obj.data['iwc_rain'][:])
                    ind_rain = np.outer(x_ind_rain, y_ind)
                    ind_rain_adv = np.outer(x_ind_rain_adv, y_ind)
                    product_dict = self._regrid_iwc(product_dict, i, j, ind, ind_rain)
                    product_adv_dict = self._regrid_iwc(product_adv_dict, i, j, ind_avd, ind_rain_adv)
                else:
                    product_dict = self._regrid_product(product_dict, i, j, ind)
                    product_adv_dict = self._regrid_product(product_adv_dict, i, j, ind_avd)
        self._append_data_to_object([product_dict, product_adv_dict])

    def _get_method_storage(self):
        if self.obs is 'cf':
            return self._cf_method_storage()
        if self.obs is 'iwc':
            return self._iwc_method_storage()
        return self._general_method_storage()

    def _cf_method_storage(self):
        cf_dict = {'cf_V': np.zeros(self.model_height.shape),
                   'cf_A': np.zeros(self.model_height.shape)}
        cf_adv_dict = {'cf_V_adv': np.zeros(self.model_height.shape),
                       'cf_A_adv': np.zeros(self.model_height.shape)}
        return cf_dict, cf_adv_dict

    def _iwc_method_storage(self):
        iwc_dict = {'iwc': np.zeros(self.model_height.shape),
                    'iwc_mask': np.zeros(self.model_height.shape),
                    'iwc_att': np.zeros(self.model_height.shape),
                    'iwc_rain': np.zeros(self.model_height.shape)}
        iwc_adv_dict = {'iwc_adv': np.zeros(self.model_height.shape),
                    'iwc_mask_adv': np.zeros(self.model_height.shape),
                    'iwc_att_adv': np.zeros(self.model_height.shape),
                    'iwc_rain_adv': np.zeros(self.model_height.shape)}
        return iwc_dict, iwc_adv_dict

    def _general_method_storage(self):
        dict = {f'{self.obs}': np.zeros(self.model_height.shape)}
        adv_dict = {f'{self.obs}_adv': np.zeros(self.model_height.shape)}
        return dict, adv_dict

    def _regrid_cf(self, array_dict, i, j, data):
        for key in array_dict.keys():
            storage = array_dict[key]
            if np.any(data):
                if '_A' in key:
                    storage[i, j] = np.mean(np.sum(data, 1) > 0)
                    storage[i, j] = np.mean(data)
            else:
                storage[i, j] = np.nan
            array_dict[key] = storage
        return array_dict

    def _reshape_data_to_window(self, ind, x_ind, y_ind):
        window_size = tl.get_obs_window_size(x_ind, y_ind)
        if np.any(window_size):
            return self.obs_data[ind].reshape(window_size)
        return []

    def _regrid_iwc(self, array_dict, i, j, ind, ind_rain):
        for key in array_dict.keys():
            storage = array_dict[key]
            if 'rain' in key:
                storage[i, j] = np.mean(self.obs_data[ind])
            if 'att' in key:
                iwc_att = self.obs_obj.data['iwc_att'][:]
                storage[i, j] = np.mean(iwc_att[ind_rain])
            if 'mask' in key:
                iwc_mask = self.obs_obj.data['iwc_mask'][:]
                storage[i, j] = np.mean(iwc_mask[ind_rain])
            storage[i, j] = np.mean(self.obs_data[ind_rain])
            array_dict[key] = storage
        return array_dict

    def _regrid_product(self, array_dict, i, j, ind):
        for key in array_dict.keys():
            storage = array_dict[key]
            storage[i, j] = np.mean(self.obs_data[ind])
            array_dict[key] = storage
        return array_dict

    def _append_data_to_object(self, array_list):
        for array_dict in array_list:
            for key in array_dict.keys():
                storage = array_dict[key]
                self.model_obj.append_data(storage, f"{key}_{self.model}{self.model_obj._cycle}")
