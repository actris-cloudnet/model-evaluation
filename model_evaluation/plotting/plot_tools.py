import numpy as np
import numpy.ma as ma
import netCDF4
from matplotlib import cm
from matplotlib.colors import ListedColormap
from model_evaluation.model_metadata import MODELS


def parse_wanted_names(nc_file, name, model):
    """Returns standard and advection lists of product types to plot"""
    names = netCDF4.Dataset(nc_file).variables.keys()
    standard_n = [n for n in names if name in n and 'adv' not in n]
    advection_n = [n for n in names if name in n and 'adv' in n]
    model_names = [n for n in names if f'{model}_{name}' in n]
    for i, model_n in enumerate(model_names):
        advection_n.insert(len(model_names)*i, model_names[i])
    return standard_n, advection_n


def parce_cycles(names, model):
    model_info = MODELS[model]
    cycles = model_info.cycle
    cycles = [x.strip() for x in cycles.split(',')]
    cycles_names = [[name for name in names if cycle in name] for cycle in cycles]
    return cycles_names


def select_vars2stats(nc_file, name):
    names = netCDF4.Dataset(nc_file).variables.keys()
    return [n for n in names if name in n]


def read_data_characters(nc_file, name, model):
    """Gets dimensions and data for plotting"""
    nc = netCDF4.Dataset(nc_file)
    data = nc.variables[name][:]
    data[data <= 0] = ma.masked
    x = nc.variables['time'][:]
    x = reshape_1d2nd(x, data)
    try:
        y = nc.variables[f'{model}_height'][:]
    except KeyError:
        model_info = MODELS[model]
        cycles = model_info.cycle
        cycles = [x.strip() for x in cycles.split(',')]
        cycle = [cycle for cycle in cycles if cycle in name]
        y = nc.variables[f'{model}_height_{cycle[0]}'][:]
    y = y / 1000
    return data, x, y


def reshape_1d2nd(one_d, two_d):
    new_arr = np.zeros(two_d.shape)
    for i in range(len(two_d[0])):
        new_arr[:, i] = one_d
    return new_arr


def create_segment_values(arrays):
    # 0=no data, 1=model, 2=intersection, 3=observation
    new_array = np.zeros(arrays[0].shape, dtype=int)
    for i, array in enumerate(arrays):
        new_array[~array] = new_array[~array] + i + 1
    new_array[new_array == 2] = 4
    new_array[new_array == 3] = 2
    new_array[new_array == 4] = 3

    colors = cm.get_cmap('YlGnBu', 256)
    newcolors = colors(np.linspace(0, 1, 256))
    cmap = ListedColormap(['whitesmoke', 'khaki', newcolors[90], newcolors[140]])
    return new_array, cmap

