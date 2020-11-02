import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import netCDF4
from ..plotting.plot_meta import ATTRIBUTES
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cloudnetpy.plotting.plotting import _set_ax, _set_labels, _handle_saving, _generate_log_cbar_ticklabel_list, _lin2log


def generate_quick_plot(nc_file, product, model, save_path=None, show=True):
    """Read files dimensions and generates figure from all data parameters"""
    names_sta, names_adv = parse_wanted_names(nc_file, product)
    for i, names in enumerate([names_sta, names_adv]):
        fig, ax = initialize_figure(len(names))
        for j, name in enumerate(names):
            variable_info = ATTRIBUTES[product]
            _set_ax(ax[j], 12)
            _set_title(ax[j], name, product, variable_info)
            data, x, y = read_data_characters(nc_file, name, model)
            plot_data_quick_look(ax[j], data, (x, y), variable_info)
        casedate = _set_labels(fig, ax[j], nc_file)
        if i == 1:
            product = product + '_adv'
        _handle_saving(None, save_path, show, 200, casedate, [product, model])


def generate_single_plot(nc_file, product, name, model, save_path=None, show=True):
    variable_info = ATTRIBUTES[product]
    fig, ax = initialize_figure(1)
    _set_ax(ax[0], 12)
    _set_title(ax[0], name, product, variable_info)
    data, x, y = read_data_characters(nc_file, name, model)
    plot_data_quick_look(ax[0], data, (x, y), variable_info)
    casedate = _set_labels(fig, ax[0], nc_file)
    _handle_saving(None, save_path, show, 200, casedate, name)


def parse_wanted_names(nc_file, name):
    names = netCDF4.Dataset(nc_file).variables.keys()
    standard_n = [n for n in names if name in n and 'adv' not in n]
    advection_n = [n for n in names if name in n and 'adv' in n]
    advection_n.insert(0, standard_n[0])
    return standard_n, advection_n


def plot_data_quick_look(ax, data, axes, variable_info):
    vmin, vmax = variable_info.plot_range
    if variable_info.plot_scale == 'logarithmic':
        data, vmin, vmax = _lin2log(data, vmin, vmax)

    cmap = plt.get_cmap(variable_info.cbar, 22)
    pl = ax.pcolormesh(*axes, data, vmin=vmin, vmax=vmax, cmap=cmap)
    colorbar = _init_colorbar(pl, ax)
    #TODO: Uudelleen formatoidaan tick labelit siistimmiksi
    if variable_info.plot_scale == 'logarithmic':
        tick_labels = _generate_log_cbar_ticklabel_list(vmin, vmax)
        colorbar.set_ticks(np.arange(vmin, vmax+1))
        colorbar.ax.set_yticklabels(tick_labels)

    colorbar.set_label(variable_info.clabel, fontsize=13)


def _set_title(ax, field_name, product, variable_info):
    parts = field_name.split('_')
    if parts[0] == product:
        title = get_product_title(field_name, variable_info)
        if product is 'cf':
            title = get_cf_title(field_name, variable_info)
        if product is 'iwc':
            title = get_iwc_title(field_name, variable_info)
        if 'adv' in field_name:
            adv = ' Downsampled using advection time'
            ax.text(0.9, -0.13, adv, size=12, ha="center",
                    transform=ax.transAxes)
        ax.set_title(title, fontsize=14)
    else:
        name = variable_info.name
        model = parts[0]
        if len(parts) > 3:
            model = f"{parts[0]} cycle {parts[-1]}"
        ax.set_title(f"{name} of {model}", fontsize=14)


def get_cf_title(field_name, variable_info):
    parts = field_name.split('_')
    name = variable_info.name
    model = parts[-1]
    if len(parts) > 3 and 'adv' not in field_name:
        model = f"{parts[-2]} cycle {parts[-1]}"
    if len(parts) > 4 and 'adv' in field_name:
        model = f"{parts[-2]} cycle {parts[-1]}"
    title = f'{name}, area downsampled from {model}'
    if 'V' in field_name:
        title = f'{name}, volume downsampled from {model}'
    return title


def get_iwc_title(field_name, variable_info):
    parts = field_name.split('_')
    name = variable_info.name
    model = parts[-1]
    if len(parts) > 3 and 'adv' not in field_name: # TODO: parempi menetelmä
        model = f"{parts[-2]} cycle {parts[-1]}"
    if len(parts) > 4 and 'adv' in field_name:
        model = f"{parts[-2]} cycle {parts[-1]}"
    title = f'{name} downsampled from {model}'
    if 'mask' in field_name:
        title = f'Masked {name}, downsampled from {model}'
    if 'att' in field_name:
        title = f'{name} with good attenuation, downsampled from {model}'
    if 'rain' in field_name:
        title = f'{name} with rain, downsampled from {model}'
    return title


def get_product_title(field_name, variable_info):
    parts = field_name.split('_')
    name = variable_info.name
    model = parts[-1]
    if len(parts) > 2 and 'adv' not in field_name:
        model = f"{parts[-2]} cycle {parts[-1]}"
    if len(parts) > 3 and 'adv' in field_name:
        model = f"{parts[-2]} cycle {parts[-1]}"
    title = f'{name} downsampled from {model}'
    return title


def read_data_characters(nc_file, name, model):
    nc = netCDF4.Dataset(nc_file)
    data = nc.variables[name][:]
    data[data <= 0] = ma.masked
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
    fig, axes = plt.subplots(n_subplots, 1, figsize=(16, 4 + (n_subplots - 1) * 4.8))
    fig.subplots_adjust(left=0.06, right=0.73)
    if n_subplots == 1:
        axes = [axes]
    return fig, axes


def _init_colorbar(plot, axis):
    divider = make_axes_locatable(axis)
    cax = divider.append_axes("right", size="1%", pad=0.25)
    return plt.colorbar(plot, fraction=1.0, ax=axis, cax=cax)
