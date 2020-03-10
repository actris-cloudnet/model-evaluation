import netCDF4
from cloudnetpy import utils, output
from cloudnetpy.products import product_tools
from model_evaluation import version
from model_evaluation.metadata import MODEL_ATTRIBUTES, CYCLE_ATTRIBUTES


def update_attributes(cloudnet_variables, attributes):
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
        elif key.split('_', x)[1] in attributes:
            cloudnet_variables[key].set_attributes(attributes[key.split('_', x)[1]])
        elif key.split('_', x)[1] in CYCLE_ATTRIBUTES:
            cloudnet_variables[key].set_attributes(CYCLE_ATTRIBUTES[key.split('_', x)[1]])


def save_model_file(id_mark, obj, file_name):
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
    output.add_file_type(root_group, id_mark)
    root_group.title = f"Model data of {id_mark.capitalize()} from {obj.dataset.location}"
    root_group.source = f"{obj._model} file: {product_tools.get_source(obj)}"
    output.copy_global(obj.dataset, root_group, ('location', 'day', 'month', 'year'))
    output.merge_history(root_group, id_mark, obj)
    root_group.close()
    

def add_var2ncfile(obj, file_name):
    nc_file = netCDF4.Dataset(file_name, 'r+', format='NETCDF4_CLASSIC')
    try:
        _write_vars2nc(nc_file, obj.data)
    except RuntimeError:
        for key in obj.data:
            nc_file.variables[key][:] = obj.data[key][:]
            for attr in obj.data[key].fetch_attributes():
                setattr(nc_file.variables[key], attr, getattr(obj.data[key], attr))
    nc_file.close()


def _init_file(file_name, dimensions, obs):
    """Initializes a Cloudnet file for writing.

    Args:
        file_name (str): File name to be generated.
        dimensions (dict): Dictionary containing dimension for this file.
        obs (dict): Dictionary containing :class:`CloudnetArray` instances.

    """
    root_group = netCDF4.Dataset(file_name, 'w', format='NETCDF4_CLASSIC')
    for key, dimension in dimensions.items():
        root_group.createDimension(key, dimension)
    _write_vars2nc(root_group, obs)
    _add_standard_global_attributes(root_group)
    return root_group


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
        nc_variable = rootgrp.createVariable(obj.name, obj.data_type, size,
                                             zlib=True)
        nc_variable[:] = obj.data
        for attr in obj.fetch_attributes():
            setattr(nc_variable, attr, getattr(obj, attr))


def _add_standard_global_attributes(root_group):
    root_group.Conventions = 'CF-1.7'
    root_group.model_evaluation_version = version.__version__
    root_group.file_uuid = utils.get_uuid()
