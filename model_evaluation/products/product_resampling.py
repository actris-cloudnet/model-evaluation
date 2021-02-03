import sys
import os
from pathlib import Path
import configparser
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.model_products import ModelManager
import model_evaluation.products.tools as tl
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.products.grid_methods import ProductGrid
from model_evaluation.plotting.plotting import generate_quick_plot, generate_single_plot

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

<<<<<<< HEAD
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))

=======
>>>>>>> a3513da... Cleaning processing

def process_observation_resample2model(model, obs, model_files, product_file, output_file):
    """Main function to generate downsampled observations to match model grid.

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
        print(m_file)
        model_obj = ModelManager(m_file, model, output_file, obs)
        ProductGrid(model_obj, product_obj)
        update_attributes(model_obj.data)
        if os.path.isfile(output_file) is False:
            tl.add_date(model_obj, product_obj)
            save_modelfile(f"{model}_products", model_obj, model_files, output_file)
        else:
            add_var2ncfile(model_obj, output_file)


def main():
    """Example processing of product downsampling system including vizualization process"""
    root = os.path.split(Path(__file__).parent)[0]
    root = os.path.split(root)[0]
    fname = f'{root}/test_files/20190517_mace-head_ecmwf.nc'
    cf_input = f'{root}/test_files/categorize.nc'
    cf_output = f'{root}/test_files/test_input_ecmwf_cf.nc'
    iwc_input = f'{root}/test_files/iwc.nc'
    iwc_output = f'{root}/test_files/test_input_ecmwf_iwc.nc'
    lwc_input = f'{root}/test_files/lwc.nc'
    lwc_output = f'{root}/test_files/test_input_ecmwf_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]
    save_path = f'{root}/plots/'

    for product, product_file, output_file in zip(['cf', 'iwc', 'lwc'], input_files, output_files):
        process_observation_resample2model('ecmwf', product, [fname], product_file, output_file)
        generate_quick_plot(output_file, product, 'ecmwf', save_path=save_path, show=True)
        generate_single_plot(output_file, product, f'ecmwf_{product}', 'ecmwf', save_path=save_path)
        if product == 'cf':
            generate_single_plot(output_file, product, f'{product}_V_ecmwf', 'ecmwf', save_path=save_path)
            generate_single_plot(output_file, product, f'{product}_V_adv_ecmwf', 'ecmwf', save_path=save_path)
        else:
            generate_single_plot(output_file, product, f'{product}_ecmwf', 'ecmwf', save_path=save_path)
            generate_single_plot(output_file, product, f'{product}_adv_ecmwf', 'ecmwf', save_path=save_path)


if __name__ == "__main__":
    main()
