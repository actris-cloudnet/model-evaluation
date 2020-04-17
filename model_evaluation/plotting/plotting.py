# generate here all plotting functions needed
import numpy as np
import matplotlib.pyplot as plt
import netCDF4


def generate_quick_plot(nc_file, name, save_path=None, show=True):
    """Read files dimensions and generates simple plot from data"""
    data, x, y = read_data_characters(nc_file, name)
    # Alustetaan kuva tässä vaiheessa
    # Luodaan plotti tässä vaiheessa
        # Tämän sisällä fiksaillaan myös labelit yms. kuvan kannalta tarpeelliset asiat
    # Jos Subplot?, halutaanko määrittää
    # Fiksaillaan yleiskuvan setti
    # Näytetään jos True
    # Talleteaan, jos polku olemassa


def read_data_characters(nc_file, name):
    nc = netCDF4.Dataset(nc_file)
    data = nc.variables[name][:]
    x = nc.variables['time'][:]
    y = nc.variables[f'{name}_height'][:]
    return data, x, y


def initialize_figure():
    """ Set up fig and ax object, if subplot"""
    print("")
