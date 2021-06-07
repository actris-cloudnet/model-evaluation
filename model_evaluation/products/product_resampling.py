import os
import model_evaluation.products.tools as tl
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.model_products import ModelManager
from model_evaluation.products.advance_methods import AdvanceProductMethods
from model_evaluation.file_handler import update_attributes, save_downsampled_file, add_var2ncfile, add_time_attribute
from model_evaluation.products.grid_methods import ProductGrid


def process_observation_resample2model(model: str,
                                       obs: str,
                                       model_files: list,
                                       product_file: str,
                                       output_file: str):
    """ Main function to generate downsampled observations to match model grid.
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
        AdvanceProductMethods(model_obj, m_file, product_obj)
        ProductGrid(model_obj, product_obj)
        attributes = add_time_attribute(product_obj.date)
        update_attributes(model_obj.data, attributes)
        if os.path.isfile(output_file) is False:
            tl.add_date(model_obj, product_obj)
            save_downsampled_file(f"{obs}_{model}", output_file, (model_obj, product_obj),
                                  (model_files, product_file))
        else:
            add_var2ncfile(model_obj, output_file)
