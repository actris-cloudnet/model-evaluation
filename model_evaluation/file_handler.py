import os
import netCDF4
from datetime import datetime
from cloudnetpy import utils, output
from model_evaluation import version
from model_evaluation.products.model_products import ModelManager
from model_evaluation.metadata import MetaData, MODEL_ATTRIBUTES, CYCLE_ATTRIBUTES, MODEL_L3_ATTRIBUTES, \
    REGRID_PRODUCT_ATTRIBUTES


def update_attributes(model_downsample_variables: dict, attributes: dict):
    """Overrides existing CloudnetArray-attributes.
    Overrides existing attributes using hard-coded values.
    New attributes are added.
    Args:
        model_downsample_variables (dict): Array instances.
        attributes (dict): Product-specific attributes.
    """
    # TODO: Change name order: model_cycle_product_method
    for key in model_downsample_variables:
        x = len(key.split('_')) - 1
        key_parts = key.split('_', x)
        if key in list(attributes.keys()):
            model_downsample_variables[key].set_attributes(attributes[key])
        if key in MODEL_ATTRIBUTES:
            model_downsample_variables[key].set_attributes(MODEL_ATTRIBUTES[key])
        elif '_'.join(key_parts[0:-1]) in REGRID_PRODUCT_ATTRIBUTES:
            model_downsample_variables[key].set_attributes(REGRID_PRODUCT_ATTRIBUTES['_'.join(key_parts[0:-1])])
        elif '_'.join(key_parts[0:-2]) in REGRID_PRODUCT_ATTRIBUTES:
            model_downsample_variables[key].set_attributes(REGRID_PRODUCT_ATTRIBUTES['_'.join(key_parts[0:-2])])
        elif key_parts[1] in MODEL_L3_ATTRIBUTES:
            try:
                model_downsample_variables[key].set_attributes(MODEL_L3_ATTRIBUTES['_'.join(key_parts[1:])])
            except KeyError:
                model_downsample_variables[key].set_attributes(MODEL_L3_ATTRIBUTES[key_parts[1]])
        elif '_'.join(key_parts[1:]) in CYCLE_ATTRIBUTES:
            model_downsample_variables[key].set_attributes(CYCLE_ATTRIBUTES['_'.join(key_parts[1:])])
        elif '_'.join(key_parts[1:-1]) in CYCLE_ATTRIBUTES:
            model_downsample_variables[key].set_attributes(CYCLE_ATTRIBUTES['_'.join(key_parts[1:-1])])


def save_downsampled_file(id_mark: str,
                          file_name: str,
                          objects: tuple,
                          files: tuple):
    """Saves a standard downsampled product file.

    Args:
        id_mark (str): File identifier, format "(product name)_(model name)"
        file_name (str): Name of the output file to be generated
        objects (tuple): Include two objects: The :class:'ModelManager' and
                      The :class:'ObservationManager.
        files (tuple): Includes two sourcefile group: List of model file(s) used
                       for processing output file and Cloudnet L2 product file
    """
    obj = objects[0]
    dimensions = {'time': len(obj.time),
                  'level': len(obj.data['level'][:])}
    root_group = output.init_file(file_name, dimensions, obj.data)
    _add_standard_global_attributes(root_group)
    output.add_file_type(root_group, id_mark)
    root_group.title = f"Downsampled {id_mark.capitalize().replace('_', ' of ')} from {obj.dataset.location}"
    _add_source(root_group, objects, files)
    output.copy_global(obj.dataset, root_group, ('location', 'day', 'month', 'year'))
    try:
        obj.dataset.day
    except AttributeError:
        root_group.year, root_group.month, root_group.day = obj.date
    output.merge_history(root_group, id_mark, obj)
    root_group.close()


def add_var2ncfile(obj: ModelManager, file_name: str):
    nc_file = netCDF4.Dataset(file_name, 'r+', format='NETCDF4_CLASSIC')
    _write_vars2nc(nc_file, obj.data)
    nc_file.close()


def _write_vars2nc(rootgrp: netCDF4.Dataset, cloudnet_variables: dict):
    """Iterates over Cloudnet instances and write to given rootgrp."""

    def _get_dimensions(array):
        """Finds correct dimensions for a variable."""
        if utils.isscalar(array):
            return ()
        variable_size = ()
        file_dims = rootgrp.dimensions
        array_dims = array.shape
        for length in array_dims:
            dim = [key for key in file_dims.keys()
                   if file_dims[key].size == length][0]
            variable_size = variable_size + (dim,)
        return variable_size

    for key in cloudnet_variables:
        obj = cloudnet_variables[key]
        size = _get_dimensions(obj.data)
        try:
            nc_variable = rootgrp.createVariable(obj.name, obj.data_type, size,
                                                 zlib=True)
            nc_variable[:] = obj.data
            for attr in obj.fetch_attributes():
                setattr(nc_variable, attr, getattr(obj, attr))
        except RuntimeError:
            continue


def _add_standard_global_attributes(root_group: netCDF4.Dataset):
    root_group.Conventions = 'CF-1.7'
    root_group.model_evaluation_version = version.__version__
    root_group.file_uuid = utils.get_uuid()


def _add_source(root_ground: netCDF4.Dataset, objects: tuple, files: tuple):
    """generates source info for multiple files"""
    model, obs = objects
    model_files, obs_file = files
    source = f"Observation file: {os.path.basename(obs_file)}"
    source += f"\n"
    source += f"{model.model} file(s): "
    for i, f in enumerate(model_files):
        source += f"{os.path.basename(f)}"
        if i < len(model_files) - 1:
            source += f"\n"
    root_ground.source = source


def add_time_attribute(date: datetime) -> dict:
    """"Adds time attribute with correct units.
    Args:
        attributes: Attributes of variables.
        date: Date as Y M D 0 0 0.
    Returns:
        dict: Same attributes with 'time' attribute added.
    """
    d = date.strftime('%y.%m.%d')
    attributes = {}
    attributes['time'] = MetaData(units=f'hours since {d} 00:00:00')
    return attributes
