# generate here all plotting functions needed
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import netCDF4


def generate_quick_plot(nc_file, name, model, save_path=None, show=True):
    """Read files dimensions and generates simple plot from data"""
    names = parse_wanted_names(nc_file, name)
    fig, ax = initialize_figure(len(names[1:2]))
    for i, n in enumerate(names[1:2]):
        data, x, y = read_data_characters(nc_file, n, model)
        plot_quick_look(ax[i], data, x, y)
    if show:
        plt.show()
    plt.savefig(f"{save_path}testi_kuva_iwc.png")


def generate_single_plot(nc_file, product, name, model):
    names = parse_wanted_names(nc_file, product)
    fig, ax = initialize_figure(1)
    for n in names:
        if n == name:
            data, x, y = read_data_characters(nc_file, n, model)
            # Tässä kohtaa pitää mahdollisesti fiksailla x-, ja y-akseleita riippuen datasta
            plot_quick_look(ax[0], data, x, y)
            plt.show()


def parse_wanted_names(nc_file, name):
    names = netCDF4.Dataset(nc_file).variables.keys()
    return [n for n in names if name in n]


def plot_quick_look(ax, data, x, y):
    data[data <= 0] = ma.masked
    vmin = np.min(data)
    vmax = np.max(data)
    print(data.shape)
    print(y[0, :35])
    pl = ax.pcolormesh(data[:, :35].T)
    plt.colorbar(pl, ax=ax)


def read_data_characters(nc_file, name, model):
    nc = netCDF4.Dataset(nc_file)
    data = nc.variables[name][:]
    x = nc.variables['time'][:]
    x = reshape_1d2nd(x, data)
    y = nc.variables[f'{model}_height'][:]
    return data, x, y


def reshape_1d2nd(one_d, two_d):
    new_arr = np.zeros(two_d.shape)
    for i in range(len(two_d[0])):
        new_arr[:, i] = one_d
    return new_arr


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
