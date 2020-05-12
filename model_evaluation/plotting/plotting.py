# generate here all plotting functions needed
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import netCDF4
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cloudnetpy.plotting.plotting import _set_ax, _set_labels


def generate_quick_plot(nc_file, name, model, save_path=None, show=True):
    """Read files dimensions and generates simple plot from data"""
    """
    TODO: Things plotting shoud do:
        - Määritetään kuva (luodaan fig) x
        - Asetetaan ax:lle otsikko ja labelit x
        - Editoidaan dataa tarvittaessa, maskaus. Jo datan talletuksessa
        - plotataan x 
        - Muokataan Fig:n labelit
        - Lisätään Fig:in otsikko, jos tarve
        - Talletetaan kuva
    """
    names = parse_wanted_names(nc_file, name)
    fig, ax = initialize_figure(len(names[0:2]))
    for i, n in enumerate(names[0:2]):
        data, x, y = read_data_characters(nc_file, n, model)
        plot_data_quick_look(ax[i], data, x, y)
    if show:
        plt.show()
    plt.savefig(f"{save_path}testi_kuva_iwc.png")


def generate_single_plot(nc_file, product, name, model):
    names = parse_wanted_names(nc_file, product)
    fig, ax = initialize_figure(1)
    for n in names:
        if n == name:
            _set_ax(ax[0], 12000)
            #_set_title(ax[0], n, f' from {model}')
            data, x, y = read_data_characters(nc_file, n, model)
            data[data < 0] = ma.masked
            # Tässä kohtaa pitää mahdollisesti fiksailla x-, ja y-akseleita riippuen datasta
            plot_data_quick_look(ax[0], data, x, y)
            plt.show()


def parse_wanted_names(nc_file, name):
    names = netCDF4.Dataset(nc_file).variables.keys()
    return [n for n in names if name in n]


def plot_data_quick_look(ax, data, *axes):
    # variable_info = ATTRIBUTE[product]
    # plot_info = PLOT_TYPE[type]
    #vmin, vmax = variable_info.plot_range
    #cmap = plt.get_cmap(variable_info.cmap, 22)
    cmap = plt.get_cmap('Blues', 22)
    vmin = 0.0
    vmax = 1.7e-5
    pl = ax.pcolormesh(*axes, data, vmin=vmin, vmax=vmax, cmap=cmap)
    colorbar = _init_colorbar(pl, ax)
    #TODO: Uudelleen formatoidaan tick labelit siistimmiksi
    #colorbar.set_ticks(np.arange(vmin, vmax))
    #colorbar.set_label(variables.clabel, fontsize=13)
    colorbar.set_label('kg m$^{-3}$', fontsize=13)


def _set_title(ax, field_name, identifier=" from CloudnetPy"):
    ax.set_title(f"{field_name}{identifier}", fontsize=14)


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


def _init_colorbar(plot, axis):
    divider = make_axes_locatable(axis)
    cax = divider.append_axes("right", size="1%", pad=0.25)
    return plt.colorbar(plot, fraction=1.0, ax=axis, cax=cax)
