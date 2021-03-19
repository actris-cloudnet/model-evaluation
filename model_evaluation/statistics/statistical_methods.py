from model_evaluation.statistics.process_day_analysis import DataGroup


class DayStatistics:
    def __init__(self, product, data_obj):
        """
        Class that generates statistical analysis for day scale products.
        The point is to analyze and point out the best simulation-observation
        combination. So which is the best resampled observations match with simulations?

        Args:
            product (str): the name of observed product
            data_obj (object): The :class:'DataManager' object
        """
        self.product = product
        self.data_obj = data_obj
        self.model_run = data_obj.group.keys()
        self.group = data_obj.group


    def generate_day_statistics(self):
        print("")
        for run in self.model_run:
            data_group = self.group[run]
            # Talletetaan alla olevalla tyylillä
            #self.data_obj.append()
            # Tällä tavalla kaikki syklit tulee samaan tiedostoon


def correlation():
    print("")


def relative_error():
    print("")


def histogram():
    print("")


def bias():
    print("")


def verification():
    print("")


def timeseries():
    print("")
    # Voi olla, että tästä tulee oma luokka tai tällä on submetodeja


def vertical_profile():
    print("")
    # Voi olla, että tästä tulee oma luokka tai tällä on submetodeja

