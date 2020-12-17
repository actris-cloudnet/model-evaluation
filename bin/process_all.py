import sys
import os
from pathlib import Path
import configparser
from model_evaluation.products.product_resampling import process_observation_resample2model
from model_evaluation.plotting.plotting import generate_quick_plot, generate_single_plot

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.split(PATH)[0]
CONF = configparser.ConfigParser()
CONF.optionxform = str
CONF.read(os.path.join(PATH, 'level3.ini'))


def main():
    """Example processing of product downsampling system including vizualization process"""
    fname = f'{PATH}/test_files/20190517_mace-head_ecmwf.nc'
    cf_input = f'{PATH}/test_files/categorize.nc'
    cf_output = f'{PATH}/test_files/test_input_ecmwf_cf.nc'
    iwc_input = f'{PATH}/test_files/iwc.nc'
    iwc_output = f'{PATH}/test_files/test_input_ecmwf_iwc.nc'
    lwc_input = f'{PATH}/test_files/lwc.nc'
    lwc_output = f'{PATH}/test_files/test_input_ecmwf_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]
    save_path = f'{PATH}/plots/'

    for product, product_file, output_file in zip(['cf', 'iwc', 'lwc'], input_files, output_files):
        process_observation_resample2model('ecmwf', product, [fname], product_file, output_file)
        generate_quick_plot(output_file, product, 'ecmwf', save_path=save_path)
        generate_single_plot(output_file, product, f'ecmwf_{product}', 'ecmwf', save_path=save_path)
        if product == 'cf':
            generate_single_plot(output_file, product, f'{product}_V_ecmwf', 'ecmwf', save_path=save_path)
            generate_single_plot(output_file, product, f'{product}_V_adv_ecmwf', 'ecmwf', save_path=save_path)
        else:
            generate_single_plot(output_file, product, f'{product}_ecmwf', 'ecmwf', save_path=save_path)
            generate_single_plot(output_file, product, f'{product}_adv_ecmwf', 'ecmwf', save_path=save_path)


if __name__ == "__main__":
    main()
