import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import netCDF4
from ..plotting.plot_meta import ATTRIBUTES
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cloudnetpy.plotting.plotting import _set_ax, _set_labels, _handle_saving


def generate_quick_plot(nc_file, name, model, save_path=None, show=True):
    """Read files dimensions and generates simple plot from data"""
    names = parse_wanted_names(nc_file, name)
    fig, ax = initialize_figure(len(names))
    for i, n in enumerate(names):
        variable_info = ATTRIBUTES[name]
        _set_ax(ax[i], 12)
        _set_title(ax[i], n, variable_info)
        data, x, y = read_data_characters(nc_file, n, model)
        plot_data_quick_look(ax[i], data, (x, y), variable_info)
    casedate = _set_labels(fig, ax[i], nc_file)
    _handle_saving(None, save_path, show, 200, casedate, [name, model])


def generate_single_plot(nc_file, product, name, model, save_path=None, show=True):
    names = parse_wanted_names(nc_file, product)
    fig, ax = initialize_figure(1)
    for n in names:
        if n == name:
            variable_info = ATTRIBUTES[product]
            _set_ax(ax[0], 12)
            _set_title(ax[0], n, variable_info)
            data, x, y = read_data_characters(nc_file, n, model)
            plot_data_quick_look(ax[0], data, (x, y), variable_info)
    casedate = _set_labels(fig, ax[0], nc_file)
    _handle_saving(None, save_path, show, 200, casedate, n)


def parse_wanted_names(nc_file, name):
    names = netCDF4.Dataset(nc_file).variables.keys()
    return [n for n in names if name in n]


def plot_data_quick_look(ax, data, axes, variable_info):
    vmin, vmax = variable_info.plot_range
    cmap = plt.get_cmap(variable_info.cbar, 22)
    pl = ax.pcolormesh(*axes, data, vmin=vmin, vmax=vmax, cmap=cmap)
    colorbar = _init_colorbar(pl, ax)
    #TODO: Uudelleen formatoidaan tick labelit siistimmiksi
    colorbar.set_label(variable_info.clabel, fontsize=13)


def _set_title(ax, field_name, variable_info):
    parts = field_name.split('_')
    if parts[1] == 'obs':
        name = variable_info.name
        model = parts[-1]
        if len(parts) == 4:
            model = f"{parts[-2]} cycle {parts[-1]}"
        ax.set_title(f"Observed {name} regrid to {model}", fontsize=14)
    else:
        name = variable_info.name
        model = parts[0]
        if len(parts) == 3:
            model = f"{parts[0]} cycle {parts[-1]}"
        ax.set_title(f"Simulated {name} from {model}", fontsize=14)


def read_data_characters(nc_file, name, model):
    nc = netCDF4.Dataset(nc_file)
    data = nc.variables[name][:]
    x = nc.variables['time'][:]
    x = reshape_1d2nd(x, data)
    y = nc.variables[f'{model}_height'][:]
    y = y / 1000
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


def _init_colorbar(plot, axis):
    divider = make_axes_locatable(axis)
    cax = divider.append_axes("right", size="1%", pad=0.25)
    return plt.colorbar(plot, fraction=1.0, ax=axis, cax=cax)
