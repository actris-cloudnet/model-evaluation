# generate here all plotting functions needed
import numpy as np
import matplotlib.pyplot as plt
import netCDF4


def generate_quick_plot(nc_file, name, save_path=None, show=True):
    """Read files dimensions and generates simple plot from data"""
    # Luetaan halutut nimet filusta, koska defaultina siellä on useampia, mitä halutaan plotata
    data, x, y = read_data_characters(nc_file, name)
    fig, ax = initialize_figure(1)
    plot_quick_look(ax, data, (x, y))
    if show:
        plt.show()

def parse_wanted_names(nc_file, name):
    # Listataan halutut nimet, kyseiselle tuotteelle oikeassa muodossa
    print("")


def plot_quick_look(ax, data, *axes):
    vmin = np.min(data)
    vmax = np.max(data)
    pl = ax.pcolorfast(*axes, data, vmin=vmin, vmax=vmax, cmap='viridis')
    plt.colorbar(pl, fraction=1.0, ax=ax)


def read_data_characters(nc_file, name):
    nc = netCDF4.Dataset(nc_file)
    data = nc.variables[name][:]
    x = nc.variables['time'][:]
    y = nc.variables[f'{name}_height'][:]
    return data, x, y


def initialize_figure(n_subplots):
    """ Set up fig and ax object, if subplot"""
    print("")
    fig, axes = plt.subplots(n_subplots, 1, figsize=(16, 4 + (n_subplots - 1) * 4.8))
    fig.subplots_adjust(left=0.06, right=0.73)
    if n_subplots == 1:
        axes = [axes]
    return fig, axes


def set_labels():
    print("")
