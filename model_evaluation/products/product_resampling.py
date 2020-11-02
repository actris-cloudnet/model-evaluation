import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import configparser
from model_evaluation.products.observation_products import ObservationManager
from model_evaluation.products.model_products import ModelManager
import model_evaluation.products.tools as tl
from model_evaluation.file_handler import update_attributes, save_modelfile, add_var2ncfile
from model_evaluation.products.grid_methods import ProductGrid
from model_evaluation.plotting.plotting import generate_quick_plot, generate_single_plot


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


def process_observation_resample2model(model, obs, model_files, product_file, output_file):
    """Read observation and downsamples it to match model grid shape.
        Creates and saves file also

        Args:
            model (str): name of model
            obs (str): name of product to generate
            model_files (list): List of files from model to be generated
            product_files (str): observation to be regrided
            output_file (str): name of model output file
    """
    product_obj = ObservationManager(obs, product_file)

    for m_file in model_files:
        model_obj = ModelManager(m_file, model, output_file, obs)
        ProductGrid(model_obj, product_obj, model, obs)
        update_attributes(model_obj.data)
        if os.path.isfile(output_file) is False:
            tl.add_date(model_obj, product_obj)
            save_modelfile(f"{model}_products", model_obj, model_files, output_file)
        else:
            add_var2ncfile(model_obj, output_file)

def main():
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
        generate_quick_plot(output_file, product, 'ecmwf', save_path=save_path, show=False)
        #generate_single_plot(output_file, product, f'ecmwf_{product}', 'ecmwf')
        #generate_single_plot(output_file, product, f'{product}_ecmwf', 'ecmwf')
        #generate_single_plot(output_file, product, f'{product}_adv_ecmwf', 'ecmwf')

if __name__ == "__main__":
    main()
