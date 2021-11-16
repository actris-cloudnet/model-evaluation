import os
from pathlib import Path
import warnings
from model_evaluation.products.product_resampling import process_L3_day_product
from model_evaluation.plotting.plotting import generate_L3_day_plots


def main():
    warnings.filterwarnings('ignore')
    """Example processing of product downsampling system including visualization process"""
    root = Path(__file__).resolve().parents[1]
    save_path = f'{root}/plots/'
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    # Run without cycles
    model_file = f'{root}/test_files/20190517_mace-head_ecmwf.nc'
    cf_input = f'{root}/test_files/20190517_mace-head_categorize.nc'
    cf_output = f'{root}/test_files/20190517_mace-head_ecmwf_downsampled_cf.nc'
    iwc_input = f'{root}/test_files/20190517_mace-head_iwc-Z-T-method.nc'
    iwc_output = f'{root}/test_files/20190517_mace-head_ecmwf_downsampled_iwc.nc'
    lwc_input = f'{root}/test_files/20190517_mace-head_lwc-scaled-adiabatic.nc'
    lwc_output = f'{root}/test_files/20190517_mace-head_ecmwf_downsampled_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]

    for product, product_file, output_file in zip(['cf', 'iwc', 'lwc'],
                                                  input_files, output_files):
        process_L3_day_product('ecmwf', product, [model_file],
                               product_file, output_file)
        generate_L3_day_plots(output_file, product, 'ecmwf', save_path=save_path,)
        generate_L3_day_plots(output_file, product, 'ecmwf', fig_type='pair')
        generate_L3_day_plots(output_file, product, 'ecmwf', fig_type='single',
                              save_path=save_path)
        generate_L3_day_plots(output_file, product, 'ecmwf', fig_type='statistic',
                              stats=['area', 'error'], save_path=save_path)


    # Run with three model cycles
    model_file_cycle1 = f'{root}/test_files/20210104_ny-alesund_icon-iglo-12-23.nc'
    model_file_cycle2 = f'{root}/test_files/20210104_ny-alesund_icon-iglo-24-35.nc'
    model_file_cycle3 = f'{root}/test_files/20210104_ny-alesund_icon-iglo-36-47.nc'
    cf_input = f'{root}/test_files/20210104_ny-alesund_categorize.nc'
    cf_output = f'{root}/test_files/20210104_ny-alesund_icon_downsampled_cf.nc'
    iwc_input = f'{root}/test_files/20210104_ny-alesund_iwc-Z-T-method.nc'
    iwc_output = f'{root}/test_files/20210104_ny-alesund_icon_downsampled_iwc.nc'
    lwc_input = f'{root}/test_files/20210104_ny-alesund_lwc-scaled-adiabatic.nc'
    lwc_output = f'{root}/test_files/20210104_ny-alesund_icon_downsampled_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]

    for product, product_file, output_file in zip(['cf', 'iwc', 'lwc'],
                                                  input_files, output_files):
        process_L3_day_product('icon', product,
                               [model_file_cycle1, model_file_cycle2,
                                model_file_cycle3], product_file, output_file)
        generate_L3_day_plots(output_file, product, 'icon', save_path=save_path)
        generate_L3_day_plots(output_file, product, 'icon', save_path=save_path,
                              fig_type='single')
        generate_L3_day_plots(output_file, product, 'icon', save_path=save_path,
                              fig_type='pair')
        generate_L3_day_plots(output_file, product, 'icon', save_path=save_path,
                              fig_type='statistic', stats=['area', 'error'])


if __name__ == "__main__":
    main()
