import os
import netCDF4
from cloudnetpy import utils, output
from model_evaluation import version
from model_evaluation.metadata import MODEL_ATTRIBUTES, CYCLE_ATTRIBUTES, L3_ATTRIBUTES, PRODUCT_ATTRIBUTES


def update_attributes(cloudnet_variables):
    """Overrides existing CloudnetArray-attributes.

    Overrides existing attributes using hard-coded values.
    New attributes are added.

    Args:
        cloudnet_variables (dict): CloudnetArray instances.
        attributes (dict): Product-specific attributes.

    """
    for key in cloudnet_variables:
        x = len(key.split('_')) - 1
        if key in MODEL_ATTRIBUTES:
            cloudnet_variables[key].set_attributes(MODEL_ATTRIBUTES[key])
        elif key.split('_', x)[0] in PRODUCT_ATTRIBUTES:
            cloudnet_variables[key].set_attributes(PRODUCT_ATTRIBUTES[key.split('_', x)[0]])
        elif key.split('_', x)[1] in L3_ATTRIBUTES:
            cloudnet_variables[key].set_attributes(L3_ATTRIBUTES[key.split('_', x)[1]])
        elif key.split('_', x)[1] in CYCLE_ATTRIBUTES:
            cloudnet_variables[key].set_attributes(CYCLE_ATTRIBUTES[key.split('_', x)[1]])


def save_modelfile(id_mark, obj, model_files, file_name):
    """Saves a standard Cloudnet product file.

    Args:
        id_mark (str): File identifier, format "(model name)_product"
        obj (object): Instance containing product specific attributes: `time`,
            `dataset`, `data`.
        file_name (str): Name of the output file to be generated.
    """
    dimensions = {'time': len(obj.time),
                  'level': len(obj.dataset.variables['level'])}
    root_group = output.init_file(file_name, dimensions, obj.data)
    _add_standard_global_attributes(root_group)
    output.add_file_type(root_group, id_mark)
    root_group.title = f"Model data of {id_mark.capitalize().replace('_', ' ')} from {obj.dataset.location}"
    _add_source(root_group, obj, model_files)
    output.copy_global(obj.dataset, root_group, ('location', 'day', 'month', 'year'))
    output.merge_history(root_group, id_mark, obj)
    root_group.close()
    

def add_var2ncfile(obj, file_name):
    nc_file = netCDF4.Dataset(file_name, 'r+', format='NETCDF4_CLASSIC')
    _write_vars2nc(nc_file, obj.data)
    nc_file.close()


def _write_vars2nc(rootgrp, cloudnet_variables):
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


def _add_standard_global_attributes(root_group):
    root_group.Conventions = 'CF-1.7'
    root_group.model_evaluation_version = version.__version__
    root_group.file_uuid = utils.get_uuid()


def _add_source(root_ground, obj, model_files):
    """generates source multiple files is existing"""
    source = f"{obj._model} file(s): "
    for i, f in enumerate(model_files):
        source += f"{os.path.basename(f)}"
        if i < len(model_files) - 1:
            source += f"\n"
    root_ground.source = source
