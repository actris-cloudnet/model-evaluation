"""
This file will be used for reading and writing .nc files
DataSource class will be inside this for reading and geting data out from files

Other part of file will be similar to Output.py of CloudnetPy,
Methods, which create file, add new data to it and overwrites attributes if
necessary.

Add also needed meta data to file with this.
One method need to copy meta from given file
"""
import os
import netCDF4
from model_evaluation import utils, version
from model_evaluation.cloudnetarray import CloudnetArray


def update_attributes(cloudnet_variables, attributes):
    """Overrides existing CloudnetArray-attributes.

    Overrides existing attributes using hard-coded values.
    New attributes are added.

    Args:
        cloudnet_variables (dict): CloudnetArray instances.
        attributes (dict): Product-specific attributes.

    """
    for key in cloudnet_variables:
        if key in attributes:
            cloudnet_variables[key].set_attributes(attributes[key])
        #if key in COMMON_ATTRIBUTES:
        #    cloudnet_variables[key].set_attributes(COMMON_ATTRIBUTES[key])


def save_product_file(short_id, obj, file_name, copy_from_file=()):
    """Saves a standard Cloudnet product file.

    Args:
        short_id (str): Short file identifier, e.g. 'cv', 'lwc', 'iwc'.
        obj (object): Instance containing product specific attributes: `time`,
            `dataset`, `data`.
        file_name (str): Name of the output file to be generated.
        copy_from_file (tuple, optional): Variables to be copied from the
            given L3 product file.
    """
    identifier = _get_identifier(short_id)
    dimensions = {'time': len(obj.time),
                  'height': len(obj.dataset.variables['height'])}
    root_group = init_file(file_name, dimensions, obj.data)
    add_file_type(root_group, short_id)
    vars_from_source = ('altitude', 'latitude', 'longitude', 'time', 'height') + copy_from_file
    copy_variables(obj.dataset, root_group, vars_from_source)
    root_group.title = f"Model data of {identifier.capitalize()} from {obj.dataset.location}"
    root_group.source = f"Categorize file: {utils.get_source(obj)}"
    copy_global(obj.dataset, root_group, ('location', 'day', 'month', 'year'))
    merge_history(root_group, identifier, obj)
    root_group.close()


def _get_identifier(short_id):
    valid_ids = ('Cv', 'lwc', 'iwc')
    if short_id not in valid_ids:
        raise ValueError('Invalid product id.')
    if short_id == 'iwc':
        return 'ice water content'
    if short_id == 'lwc':
        return 'liquid water content'
    if short_id == 'cv':
        return 'cloud fraction'
    return short_id


def merge_history(root_group, file_type, *sources):
    """Merges history fields from one or several files and creates a new record.

    Args:
        root_group (netCDF Dataset): The netCDF Dataset instance.
        file_type (str): Long description of the file.
        *sources (obj): Objects that were used to generate this product. Their
            `history` attribute will be copied to the new product.

    """
    new_record = f"{utils.get_time()} - {file_type} file created"
    old_history = ''
    for source in sources:
        old_history += f"\n{source.dataset.history}"
    root_group.history = f"{new_record}{old_history}"


def init_file(file_name, dimensions, obs):
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
    root_group.cloudnetpy_version = version.__version__
    root_group.file_uuid = utils.get_uuid()


def copy_variables(source, target, var_list):
    """Copies variables (and their attributes) from one file to another.

    Args:
        source (object): Source object.
        target (object): Target object.
        var_list (list): List of variables to be copied.

    """
    for var_name, variable in source.variables.items():
        if var_name in var_list:
            var_out = target.createVariable(var_name, variable.datatype,
                                            variable.dimensions)
            var_out.setncatts({k: variable.getncattr(k)
                               for k in variable.ncattrs()})
            var_out[:] = variable[:]


def copy_global(source, target, attr_list):
    """Copies global attributes from one file to another.

    Args:
        source (object): Source object.
        target (object): Target object.
        attr_list (list): List of attributes to be copied.

    """
    for attr_name in source.ncattrs():
        if attr_name in attr_list:
            setattr(target, attr_name, source.getncattr(attr_name))


def add_file_type(root_group, file_type):
    """Adds cloudnet_file_type global attribute.

    Args:
        root_group (object): netCDF Dataset instance.
        file_type (str): Name of the Cloudnet file type.

    """
    root_group.cloudnet_file_type = file_type


class DataSource:
    """Base class for all Cloudnet measurements and model data.

    Args:
        filename (str): Calibrated instrument / model NetCDF file.
        radar (bool, optional): Indicates if data is from cloud radar.
            Default is False.

    Attributes:
        filename (str): Filename of the input file.
        dataset (Dataset): A netCDF4 Dataset instance.
        source (str): Global attribute `source` read from the input file.
        time (MaskedArray): Time array of the instrument.
        altitude (float): Altitude of instrument above mean sea level (m).
        data (dict): Dictionary containing :class:`CloudnetArray` instances.

    """
    def __init__(self, filename):
        self.filename = os.path.basename(filename)
        self.dataset = netCDF4.Dataset(filename)
        self.source = getattr(self.dataset, 'source', '')
        self.time = self._init_time()
        self.altitude = self._init_altitude()
        self.data = {}
        self._array_type = CloudnetArray

    def getvar(self, *args):
        """Returns data array from the source file variables.

        Returns just the data (and no attributes) from the original variables
        dictionary, fetched from the input NetCDF file.

        Args:
            *args: possible names of the variable. The first match is returned.

        Returns:
            MaskedArray: The actual data.

        Raises:
             RuntimeError: The variable is not found.

        """
        for arg in args:
            if arg in self.dataset.variables:
                return self.dataset.variables[arg][:]
        raise RuntimeError('Missing variable in the input file.')

    def append_data(self, array, key, name=None, units=None):
        """Adds new CloudnetVariable into `data` attribute.

        Args:
            array (ndarray): Array to be added.
            key (str): Key used with *array* when added to `data` attribute
                (which is a dictionary).
            name (str, optional): CloudnetArray.name attribute. Default value
                is *key*.
            units (str, optional): CloudnetArray.units attribute.

        """
        self.data[key] = self._array_type(array, name or key, units)

    def close(self):
        """Closes the open file."""
        self.dataset.close()

    @staticmethod
    def km2m(var):
        """Converts km to m."""
        alt = var[:]
        if var.units == 'km':
            alt *= 1000
        return alt

    @staticmethod
    def m2km(var):
        """Converts m to km."""
        alt = var[:]
        if var.units == 'm':
            alt /= 1000
        return alt

    def _init_time(self):
        time = self.getvar('time')
        if max(time) > 25:
            time = utils.seconds2hours(time)
        return time

    def _init_altitude(self):
        """Returns altitude of the instrument (m)."""
        if 'altitude' in self.dataset.variables:
            altitude_above_sea = self.km2m(self.dataset.variables['altitude'])
            return float(altitude_above_sea)
        return None

    def _netcdf_to_cloudnet(self, fields):
        """Transforms netCDF4-variables into CloudnetArrays.

        Args:
            fields (tuple): netCDF4-variables to be converted. The results are
                saved in *self.data* dictionary with *fields* strings as keys.

        Notes:
            The attributes of the variables are not copied. Just the data.

        """
        for key in fields:
            self.append_data(self.dataset.variables[key], key)

    def _unknown_to_cloudnet(self, possible_names, key, units=None):
        """Transforms single netCDF4 variable into CloudnetArray.

        Args:
            possible_names(tuple): Tuple of strings containing the possible
                names of the variable in the input NetCDF file.

            key(str): Key for self.data dictionary and name-attribute for
                the saved CloudnetArray object.

            units(str, optional): Units-attribute for the CloudnetArray object.

        """
        array = self.getvar(*possible_names)
        self.append_data(array, key, units=units)
