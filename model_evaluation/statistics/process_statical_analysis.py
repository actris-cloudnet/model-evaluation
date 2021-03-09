import sys
from pathlib import Path
#from model_evaluation.statistics.statistical_methods import DayStatistics
from cloudnetpy.categorize.datasource import DataSource

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def process_product_statistics(model, product, product_file, scale='day'):
    obj = DataManager(model, product, product_file)
    #day_stat = DayStatistics(product, obj.model, obj.)


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
