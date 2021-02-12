import os
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b91fc3f... Cleaning processing
from pathlib import Path
import configparser
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.model_products import ModelManager
import model_evaluation.products.tools as tl
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.products.grid_methods import ProductGrid
from model_evaluation.plotting.plotting import generate_quick_plot, generate_single_plot
<<<<<<< HEAD
=======
import model_evaluation.products.tools as tl
from ..products.observation_products import ObservationManager
from ..products.model_products import ModelManager
from ..file_handler import update_attributes, save_downsampled_file, add_var2ncfile
from ..products.grid_methods import ProductGrid
>>>>>>> 79ae918... Fix merge issues and improve documentation

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

<<<<<<< HEAD
<<<<<<< HEAD
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))
=======
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.model_products import ModelManager
import model_evaluation.products.tools as tl
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.products.grid_methods import ProductGrid
>>>>>>> 122b8aa... Fixes process_all script and bug in standard product downsampling

=======
>>>>>>> a3513da... Cleaning processing

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def process_observation_resample2model(model, obs, model_files, product_file, output_file):
=======
def process_observation_resample2model(model: str,
                                       obs: str,
                                       model_files: list,
                                       product_file: str,
                                       output_file: str):
>>>>>>> d46ee4a... Adds type hints for attributes of functions
    """Main function to generate downsampled observations to match model grid.
=======
def downsample_observation2model(model: str,
                               obs: str,
                               model_files: list,
                               product_file: str,
                               output_file: str):
=======
def process_observation_resample2model(model: str,
                                       obs: str,
                                       model_files: list,
                                       product_file: str,
                                       output_file: str):
>>>>>>> fed6cde... Fix histogram bins for plot
    """ Main function to generate downsampled observations to match model grid.
>>>>>>> 79ae918... Fix merge issues and improve documentation
=======
=======

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))
=======
import model_evaluation.products.tools as tl
from ..products.observation_products import ObservationManager
from ..products.model_products import ModelManager
from ..file_handler import update_attributes, save_modelfile, add_var2ncfile
from ..products.grid_methods import ProductGrid
>>>>>>> cdb269d... Changes import paths
=======
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.model_products import ModelManager
import model_evaluation.products.tools as tl
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.products.grid_methods import ProductGrid
>>>>>>> edbb462... Fixes process_all script and bug in standard product downsampling


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> b91fc3f... Cleaning processing
def process_observation_resample2model(model, obs, model_files, product_file, output_file):
=======
def process_observation_resample2model(model: str,
                                       obs: str,
                                       model_files: list,
                                       product_file: str,
                                       output_file: str):
>>>>>>> 24bb1eb... Adds type hints for attributes of functions
=======
def resample_observation2model(model: str,
                               obs: str,
                               model_files: list,
                               product_file: str,
                               output_file: str):
>>>>>>> 89306c0... Cleaning processing
=======

def process_observation_resample2model(model, obs, model_files, product_file, output_file):
>>>>>>> 4b00ebd... Improve documentation
    """Main function to generate downsampled observations to match model grid.
>>>>>>> 122b8aa... Fixes process_all script and bug in standard product downsampling

        This functio will generate nc-file of a downsampled product included all model and
        cycles information as well as resampled observations for each model and cycle grid.

        Args:
            model (str): name of model
            obs (str): name of product to generate
            model_files (list): List of files from model to be generated
            product_file (str): observation to be regrided
            output_file (str): name of model output file


        Raises:
            RuntimeError: Failed to create the resampled product file.

        Notes:
            Model files are given as list to make all different cycles to be at same nc-file.
            If list have only one element, nc-file is created, with more elements -> data is added to
            same file.

        Examples:
            >>> from model_evaluation.products.product_resampling import process_observation_resample2model
            >>> product = 'cf'
            >>> model = 'ecmwf'
            >>> model_file = 'ecmwf.nc'
            >>> input_file = 'categorize.nc'
            >>> output_file = 'cf_ecmwf.nc'
            >>> process_observation_resample2model(model, product, [model_file], input_file, output_file)

    """
    product_obj = ObservationManager(obs, product_file)
    for m_file in model_files:
        model_obj = ModelManager(m_file, model, output_file, obs)
        ProductGrid(model_obj, product_obj)
        update_attributes(model_obj.data)
        if os.path.isfile(output_file) is False:
            tl.add_date(model_obj, product_obj)
            save_modelfile(f"{model}_products", model_obj, model_files, output_file)
        else:
            add_var2ncfile(model_obj, output_file)
