import sys
import os
from pathlib import Path
from model_evaluation.statistics.statistical_methods import DayStatistics
from cloudnetpy.categorize.datasource import DataSource

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def process_product_statistics(model, product, product_file, scale='day'):
    obj = DataManager(model, product, product_file)
    day_stat = DayStatistics(product, obj)
    # Talletetaan tämä otus tiedostoksi
    # Pitää myöhemmin päättää, halutaanko data omiin tiedostoihin vai yhteen isoon


class DataGroup:
    def __init__(self, model_run, model_data, observation, observation_data):
        self.model_run = model_run
        self.model_data = model_data
        obs = observation[0]
        obs_data = observation_data[0]
        obs_adv = observation[-1]
        obs_data_adv = observation_data[-1]
        self.obs_dict = {}
        for obs, data in zip(obs, obs_data):
            self.obs_dict[obs] = data
        self.obs_dict_adv = {}
        for obs, data in zip(obs_adv, obs_data_adv):
            self.obs_dict_adv[obs] = data


class DataManager(DataSource, DataGroup):
    def __init__(self, model, product, product_file):
        super().__init__(product_file)
        self.model = model
        self.product = product
        self.file = product_file
        self.variables = self.dataset.variables.keys()
        self.group = {}
        self.get_product_variables()

    def get_product_variables(self):
        run_info = self.get_models_from_variables()
        print(run_info)
        for run, name in zip(*run_info):
            obs, obs_data = self.sort_observations(run)
            run_data = self.getvar(name)
            data_g = DataGroup(name, run_data, obs, obs_data)
            self.group[name] = data_g

    def get_models_from_variables(self):
        model_runs = []
        run_names = []
        for var in self.variables:
            if self.product in var:
                parts = var.split('_')
                if parts[0] == self.model:
                    model_runs.append('_'.join(parts[0:-1]))
                    run_names.append(var)
        return model_runs, run_names

    def sort_observations(self, model):
        obs = []
        obs_data = []
        obs_adv = []
        obs_data_adv = []
        for var in self.variables:
            if '_' + model in var:
                if 'adv' in var:
                    obs_adv.append(var)
                    obs_data_adv.append(self.getvar(var))
                else:
                    obs.append(var)
                    obs_data.append(self.getvar(var))
        return [obs, obs_adv], [obs_data, obs_data_adv]


def main():
    """Example processing of a product statistical analysing system for day level"""
    root = os.path.split(Path(__file__).parent)[0]
    root = os.path.split(root)[0]
    cf_input = f'{root}/test_files/test_input_ecmwf_cf.nc'
    cf_output = f'{root}/test_files/ecmwf_cf_statistics_day.nc'
    iwc_input = f'{root}/test_files/test_input_ecmwf_iwc.nc'
    iwc_output = f'{root}/test_files/ecmwf_iwc_statistics_day.nc'
    lwc_input = f'{root}/test_files/test_input_ecmwf_lwc.nc'
    lwc_output = f'{root}/test_files/ecmwf_lwc_statistics_day.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]
    save_path = f'{root}/plots/'
    process_product_statistics('ecmwf', 'cf', cf_input)


if __name__ == "__main__":
    main()
