import numpy as np
import numpy.ma as ma
import netCDF4
from matplotlib import cm
from typing import Tuple
from matplotlib.colors import ListedColormap
from typing import Union
from model_evaluation.model_metadata import MODELS


def parse_wanted_names(nc_file: str, name: str, model: str,
                       vars: Union[list, None] = None,
                       advance: Union[str, None] = None) -> Tuple[list, list]:
    """Returns standard and advection lists of product types to plot"""
    if vars:
        names = vars
    else:
        names = parse_dataset_keys(nc_file, name, advance, model)
    standard_n = [n for n in names if name in n and 'adv' not in n]
    standard_n = sort_model2first_element(standard_n, model)
    advection_n = [n for n in names if name in n and 'adv' in n]
    model_names = [n for n in names if f'{model}_{name}' in n]
    for i, model_n in enumerate(model_names):
        advection_n.insert(0+i, model_n)
    if len(advection_n) < len(standard_n):
        return standard_n, []
    return standard_n, advection_n


def parse_dataset_keys(nc_file: str, name: str, advance: Union[str, None],
                       model: str = "") -> list:
    names = list(netCDF4.Dataset(nc_file).variables.keys())
    if advance:
        model_vars = [n for n in names if f'{model}_{name}' in n and advance not in n]
        for m in model_vars:
            names.remove(m)
    else:
        advance = ['cirrus', 'snow']
        model_vars = [n for n in names for a in advance if f'{model}_{name}' in n and a in n]
        for m in model_vars:
            names.remove(m)
    return names


def sort_model2first_element(a: list, model: str) -> list:
    mm = [n for n in a if f"{model}_" in n and f"_{model}_" not in n]
    for i, m in enumerate(mm):
        a.remove(m)
        a.insert(0+i, m)
    return a


def sort_cycles(names: list, model: str) -> Tuple[list, list]:
    model_info = MODELS[model]
    cycles = model_info.cycle
    cycles = [x.strip() for x in cycles.split(',')]
    cycles_names = [[name for name in names if cycle in name] for cycle in cycles]
    cycles_names.sort()
    cycles_names = [c for c in cycles_names if c]
    cycles = [c for c in cycles for name in cycles_names if c in name[0]]
    return cycles_names, cycles


def select_vars2stats(nc_file: str, name: str, vars: Union[list, None] = None,
                      advance: Union[str, None] = None) -> list:
    if vars:
        names = vars
    else:
        names = parse_dataset_keys(nc_file, name, advance)
    return [n for n in names if name in n]


def read_data_characters(nc_file: str, name: str, model: str) -> Tuple:
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
        y = nc.variables[f'{model}_{cycle[0]}_height'][:]
    y = y / 1000
    try:
        mask = y.mask
        if mask.any():
            x, y, data = change2one_dim_axes(x, y, data)
    except AttributeError:
        return data, x, y
    return data, x, y


def reshape_1d2nd(one_d:  np.array, two_d:  np.array) -> np.array:
    new_arr = np.zeros(two_d.shape)
    for i in range(len(two_d[0])):
        new_arr[:, i] = one_d
    return new_arr


def create_segment_values(arrays: list) -> Tuple:
    # 0=no data, 1=model, 2=intersection, 3=observation
    new_array = np.zeros(arrays[0].shape, dtype=int)
    for i, array in enumerate(arrays):
        new_array[~array] = new_array[~array] + i + 1
    new_array[new_array == 2] = 4
    new_array[new_array == 3] = 2
    new_array[new_array == 4] = 3

    colors = cm.get_cmap('YlGnBu', 256)
    newcolors = colors(np.linspace(0, 1, 256))
    # No data, model, both, observation
    cmap = ListedColormap(['whitesmoke', 'khaki', newcolors[90], newcolors[140]])
    if len(np.unique(new_array)) < 4:
        # model, both, model comparison
        cmap = ListedColormap(['whitesmoke', 'khaki', newcolors[90]])
    return new_array, cmap


def set_yaxis(ax, max_y: float, min_y: float = 0.0):
    ax.set_ylim(min_y, max_y)
    ax.set_ylabel('Height (km)', fontsize=13)


def rolling_mean(data: np.array, n: int = 4) -> np.array:
    mmr = []
    for i in range(len(data)):
        if not data[i:i+n].mask.all():
            mmr.append(np.nanmean(data[i:i+n]))
        else:
            mmr.append(np.nan)
    return np.asarray(mmr)


def change2one_dim_axes(x: np.array, y: np.array, data: np.array) -> Tuple:
    # If any mask in x or y, change 2d to 1d axes values
    # Common shape need to match 2d data.
    for ax in [x, y]:
        try:
            mask = ax.mask
            if mask.any():
                y = [y[i] for i in range(len(y[:])) if not y[i].mask.all()]
                return x[:, 0], y[0], data.T
        except AttributeError:
            continue
    return x, y, data
