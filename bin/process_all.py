import sys
import os
from pathlib import Path
from model_evaluation.products.product_resampling import process_observation_resample2model
from model_evaluation.plotting.plotting import generate_L3_day_plots

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    """Example processing of product downsampling system including visualization process"""
    root = os.path.split(Path(__file__).parent)[0]
    save_path = f'{root}/plots/' # Create own dir

    # Run without cycles
    model_file = f'{root}/test_files/20190517_mace-head_ecmwf.nc'
    cf_input = f'{root}/test_files/categorize.nc'
    cf_output = f'{root}/test_files/test_input_ecmwf_cf.nc'
    iwc_input = f'{root}/test_files/iwc.nc'
    iwc_output = f'{root}/test_files/test_input_ecmwf_iwc.nc'
    lwc_input = f'{root}/test_files/lwc.nc'
    lwc_output = f'{root}/test_files/test_input_ecmwf_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]

    for product, product_file, output_file in zip(['cf', 'iwc', 'lwc'],
                                                  input_files, output_files):
        process_observation_resample2model('ecmwf', product, [model_file],
                                           product_file, output_file)
        generate_L3_day_plots(output_file, 'mace-head', product, 'ecmwf',
                              save_path=save_path)

    # Run with three model cycles
    model_file_cycle1 = f'{root}/test_files/20210222_norunda_harmonie-fmi-6-11.nc'
    model_file_cycle2 = f'{root}/test_files/20200501_bucharest_era5-7-18.nc'
    model_file_cycle3 = f'{root}/test_files/20201208_juelich_icon-iglo-36-47.nc'
    cf_input = f'{root}/test_files/20210222_norunda_categorize.nc'
    cf_output = f'{root}/test_files/test_input_harmonie_cf.nc'
    iwc_input = f'{root}/test_files/20201208_juelich_iwc-Z-T-method.nc'
    iwc_output = f'{root}/test_files/test_input_icon_iwc.nc'
    lwc_input = f'{root}/test_files/20201208_juelich_lwc-scaled-adiabatic.nc'
    lwc_output = f'{root}/test_files/test_input_icon_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]

    for product, product_file, output_file in zip(['cf', 'iwc', 'lwc'],
                                                  input_files, output_files):
        process_observation_resample2model('harmonie', product,
                                           [model_file_cycle1, model_file_cycle2,
                                            model_file_cycle3], product_file, output_file)
        generate_L3_day_plots(output_file, 'norunda', product, 'harmonie',
                              save_path=save_path, show=False)


if __name__ == "__main__":
    main()
