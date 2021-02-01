import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from ..statistics.statistical_methods import DayStatistics
from ..plotting.plot_meta import ATTRIBUTES
import model_evaluation.plotting.plot_tools as p_tools
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cloudnetpy.plotting.plotting import _set_ax, _set_labels, _handle_saving, _generate_log_cbar_ticklabel_list, _lin2log


<<<<<<< HEAD
def generate_quick_plot(nc_file, product, model, save_path=None, show=False):
=======
def generate_day_figures(nc_file, product, model, save_path=None, show=False):
>>>>>>> 8043b0d... Adds Statistical plotting
    """ Subplot visualization for both standard and advection downsampling.

        Generates subplot visualization of standard product and advection
        product with model data and all different downsampling methods.

        Args:
            nc_file (str): Path to source file
            product (str): Name of product wanted to plot
            model (str): Name of model which downsampling was done with
            save_path (str, optional): If not None, visualization is saved
                                       to path location
            show (bool, optional): If True, shows visualization
    """
    names_sta, names_adv = p_tools.parse_wanted_names(nc_file, product)
    for i, names in enumerate([names_sta, names_adv]):
        fig, ax = initialize_figure(len(names))
        for j, name in enumerate(names):
            variable_info = ATTRIBUTES[product]
            _set_ax(ax[j], 12)
            _set_title(ax[j], name, product, variable_info)
            data, x, y = p_tools.read_data_characters(nc_file, name, model)
            plot_data_quick_look(ax[j], data, (x, y), variable_info)
        casedate = _set_labels(fig, ax[j], nc_file)
        if i == 1:
            product = product + '_adv'
        _handle_saving(None, save_path, show, 200, casedate, [product, model])


def generate_single_plot(nc_file, product, name, model, save_path=None, show=False):
    """Generates visualization of one product

        Args:
            nc_file (str): Path to source file
            product (str): Name of product wanted to plot
            model (str): Name of model which downsampling was done with
            save_path (str, optional): If not None, visualization is saved
                                       to path location
            show (bool, optional): If True, shows visualization
    """
    variable_info = ATTRIBUTES[product]
    fig, ax = initialize_figure(1)
    _set_ax(ax[0], 12)
    _set_title(ax[0], name, product, variable_info)
    data, x, y = p_tools.read_data_characters(nc_file, name, model)
    plot_data_quick_look(ax[0], data, (x, y), variable_info)
    casedate = _set_labels(fig, ax[0], nc_file)
    _handle_saving(None, save_path, show, 200, casedate, [name])


<<<<<<< HEAD
def parse_wanted_names(nc_file, name):
    """Returns standard and advection lists of product types to plot"""
    names = netCDF4.Dataset(nc_file).variables.keys()
    standard_n = [n for n in names if name in n and 'adv' not in n]
    advection_n = [n for n in names if name in n and 'adv' in n]
    advection_n.insert(0, standard_n[0])
    return standard_n, advection_n
=======
def generate_day_statistics(nc_file, product, model, save_path=None, show=False):
    """ Subplots statistical analysis for day scale products.
>>>>>>> 8043b0d... Adds Statistical plotting

    Args:
        nc_file:
        product:
        model:
        stats (boolean):
        save_path:
        show:

<<<<<<< HEAD
=======
    Returns:

    """
    names = p_tools.select_vars2stats(nc_file, product)
    variable_info = ATTRIBUTES[product]
    stats = ['error', 'cov', 'hist']
    #stats = ['hist_vertical', 'vertical']
    #stats = ['hist']
    for i, stat in enumerate(stats):
        fig, ax = initialize_figure(len(names) - 1)
        for j, name in enumerate(names):
            data, x, y = p_tools.read_data_characters(nc_file, name, model)
            if product == 'cf' and stat == 'error':
                stat = 'aerror'
            if j == 0:
                model_data = data
            if j > 0:
                name = _get_stat_titles(name, product, variable_info)
                day_stat = DayStatistics(stat, [product, model, name], model_data,
                                         data)
                get_day_statistic_plots(ax[j-1], stat, product, day_stat, model_data,
                                        data, (x, y), variable_info)
        casedate = _set_labels(fig, ax[j-1], nc_file)
        if stat =='hist' or stat == 'vertical':
            ax[j-1].set_xlabel(variable_info.hist_x_title, fontsize=13)
        if stat == 'hist_vert':
            ax[j-1].set_xlabel('Relative frequency %', fontsize=13)
        _handle_saving(None, save_path, show, 200, casedate, [product, model, stat])


def initialize_figure(n_subplots, stat=''):
    """ Set up fig and ax object, if subplot"""
    fig, axes = plt.subplots(n_subplots, 1, figsize=(16, 4 + (n_subplots - 1) * 4.8))
    if stat == 'hist':
        fig, axes = plt.subplots(n_subplots, figsize=(16, 10))
    fig.subplots_adjust(left=0.06, right=0.73, hspace=0.3)
    if n_subplots == 1:
        axes = [axes]
    return fig, axes


>>>>>>> 8043b0d... Adds Statistical plotting
def plot_data_quick_look(ax, data, axes, variable_info):
    vmin, vmax = variable_info.plot_range
    if variable_info.plot_scale == 'logarithmic':
        data, vmin, vmax = _lin2log(data, vmin, vmax)
    cmap = plt.get_cmap(variable_info.cbar, 22)
    pl = ax.pcolormesh(*axes, data, vmin=vmin, vmax=vmax, cmap=cmap)
    colorbar = init_colorbar(pl, ax)
    if variable_info.plot_scale == 'logarithmic':
        tick_labels = _generate_log_cbar_ticklabel_list(vmin, vmax)
        colorbar.set_ticks(np.arange(vmin, vmax+1))
        colorbar.ax.set_yticklabels(tick_labels)
    ax.set_facecolor('whitesmoke')
    colorbar.set_label(variable_info.clabel, fontsize=13)


<<<<<<< HEAD
=======
def get_day_statistic_plots(ax, method, product, day_stat, model, obs, args, variable_info):
    if method == 'error' or method == 'aerror':
        plot_relative_error(ax, day_stat.stat_data.T, args, method)
        ax.set_title(day_stat.title, fontsize=14)
        _set_ax(ax, 12)
    if method == 'cov':
        plot_mask_coverage(ax, day_stat, model, obs, args)
        ax.text(0.9, -0.14, f"Common coverage: {day_stat.stat_data} %",
                size=12, ha="center", transform=ax.transAxes)
        _set_ax(ax, 12)
    if method == 'hist':
        plot_histogram(ax, day_stat, variable_info)
    if method == 'hist_vertical':
        plot_histogram_vertical(ax, day_stat, variable_info)


def plot_relative_error(ax, error, axes, method):
    pl = ax.pcolormesh(*axes, error[:-1, :-1].T, cmap='RdBu', vmin=-50, vmax=50)
    colorbar = init_colorbar(pl, ax)
    colorbar.set_label("%", fontsize=13)
    median_error = ma.median(error.compressed())
    median_error = "%.1f" % median_error
    if method == 'aerror':
        ax.text(0.9, -0.14, f"Median absolute error: {median_error} %", size=12, ha="center",
                transform=ax.transAxes)
    else:
        ax.text(0.9, -0.14, f"Median relative error: {median_error} %", size=12, ha="center",
                transform=ax.transAxes)


def plot_mask_coverage(ax, day_stat, model_data, obs_data, axes):
    data, cmap = p_tools.create_segment_values([model_data.mask, obs_data.mask])
    pl = ax.pcolormesh(*axes, data, cmap=cmap)
    colorbar = init_colorbar(pl, ax)
    colorbar.set_ticks(np.arange(1, 1, 3))
    ax.set_title(f"{day_stat.title}", fontsize=14)
    ax.set_facecolor('black')
    legend_elements = [Patch(facecolor='khaki', edgecolor='k', label='Model'),
                       Patch(facecolor=cmap(0.5), edgecolor='k', label='Common'),
                       Patch(facecolor=cmap(1.), edgecolor='k', label='Observation')]
    ax.legend(handles=legend_elements, loc='lower left', ncol=3, fontsize=12, bbox_to_anchor=(-0.0, -0.22))


def plot_histogram(ax, day_stat, variable_info):
    # TODO: Fix issues with data
    weights = np.ones_like(day_stat.stat_data[0]) / float(len(day_stat.stat_data[0]))
    pl1 = ax.hist(day_stat.stat_data[0], weights=weights, bins=1,
                  alpha=0.7, facecolor='khaki', edgecolor='k', label='Model')

    weights = np.ones_like(day_stat.stat_data[1]) / float(len(day_stat.stat_data[1]))
    pl2 = ax.hist(day_stat.stat_data[1], weights=weights,
                  alpha=0.7, facecolor='steelblue', edgecolor='k', label='Observation')
    ax.set_title(f"{day_stat.title}", fontsize=14)
    ax.set_ylabel('Relative frequency %', fontsize=13)
    #ax.xaxis.set_ticks(np.arange(variable_info.hist_limits[0],
    #                             variable_info.hist_limits[1],
    #                             variable_info.hist_limits[2]))
    ax.yaxis.grid(True, 'major')
    ax.legend(loc='upper right', fontsize=14, bbox_to_anchor=(1.08, 1.1))


def plot_histogram_vertical(ax, day_stat, variable_info):
    weights = np.ones_like(day_stat.stat_data[0]) / float(len(day_stat.stat_data[0]))
    pl1 = ax.hist(day_stat.stat_data[0], weights=weights,
                  alpha=0.7, facecolor='khaki', edgecolor='k', orientation='horizontal')

    weights = np.ones_like(day_stat.stat_data[1]) / float(len(day_stat.stat_data[1]))
    pl2 = ax.hist(day_stat.stat_data[1], weights=weights,
                  alpha=0.7, facecolor='steelblue', edgecolor='k', orientation='horizontal')
    ax.xaxis.set_ticks(np.arange(0.0, 1.1, 0.1))
    ax.yaxis.set_ticks(np.arange(0, 12, 1))
    ax.set_xlabel('Relative frequency %', fontsize=13)

    ax.xaxis.grid(True, 'major')
    ax.yaxis.grid(True, 'major')


>>>>>>> 8043b0d... Adds Statistical plotting
def _set_title(ax, field_name, product, variable_info):
    """Generates subtitles for different product types"""
    parts = field_name.split('_')
    if parts[0] == product:
        title = get_product_title(field_name, variable_info)
        if product == 'cf':
            title = get_cf_title(field_name, variable_info)
        if product == 'iwc':
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
    title = f'{name}, downsampled by area from {model}'
    if 'V' in field_name:
        title = f'{name}, downsampled by volume from {model}'
    return title


def get_iwc_title(field_name, variable_info):
    parts = field_name.split('_')
    name = variable_info.name
    model = parts[-1]
    if 'att' in field_name:
        if len(parts) > 3 and 'adv' not in field_name:
            model = f"{parts[-2]} cycle {parts[-1]}"
        if len(parts) > 4 and 'adv' in field_name:
            model = f"{parts[-2]} cycle {parts[-1]}"
        title = f'{name} with good attenuation, downsampled from {model}'
    elif 'rain' in field_name:
        if len(parts) > 3 and 'adv' not in field_name:
            model = f"{parts[-2]} cycle {parts[-1]}"
        if len(parts) > 4 and 'adv' in field_name:
            model = f"{parts[-2]} cycle {parts[-1]}"
        title = f'{name} with rain, downsampled from {model}'
    else:
        if len(parts) > 2 and 'adv' not in field_name:
            model = f"{parts[-2]} cycle {parts[-1]}"
        if len(parts) > 3 and 'adv' in field_name:
            model = f"{parts[-2]} cycle {parts[-1]}"
        title = f'{name} downsampled from {model}'
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


<<<<<<< HEAD
def read_data_characters(nc_file, name, model):
    """Gets dimensions and data for plotting"""
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
=======
def _get_stat_titles(field_name, product, variable_info):
    title = get_product_title_stat(field_name, variable_info)
    if product == 'cf':
        title = get_cf_title_stat(field_name, variable_info)
    if product == 'iwc':
        title = get_iwc_title_stat(field_name, variable_info)
    if 'adv' in field_name:
        adv = ' (Advection time)'
        return f"{title}{adv}"
    return title


def get_cf_title_stat(field_name, variable_info):
    parts = field_name.split('_')
    name = variable_info.name
    title = f'{name} area'
    if 'V' in field_name:
        title = f'{name} volume'
    return title


def get_iwc_title_stat(field_name, variable_info):
    name = variable_info.name
    if 'att' in field_name:
        title = f'{name} with good attenuation'
    elif 'rain' in field_name:
        title = f'{name} with rain'
    else:
        title = f'{name}'
    return title


def get_product_title_stat(field_name, variable_info):
    name = variable_info.name
    title = f'{name}'
    return title
>>>>>>> 8043b0d... Adds Statistical plotting


def init_colorbar(plot, axis):
    divider = make_axes_locatable(axis)
    cax = divider.append_axes("right", size="1%", pad=0.25)
    return plt.colorbar(plot, fraction=1.0, ax=axis, cax=cax)
