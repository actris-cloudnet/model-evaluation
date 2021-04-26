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
    """
    output_files =[f'{root}/test_files/20210222_palaiseau_icon_downsampled_cf.nc',
                   f'{root}/test_files/20210222_palaiseau_icon_downsampled_iwc.nc',
                   f'{root}/test_files/20210222_palaiseau_icon_downsampled_lwc.nc']

    for product, output_file in zip(['cf', 'iwc', 'lwc'], output_files):
        generate_L3_day_plots(output_file, 'palaiseau', product, 'icon',
                              fig_type='pair', save_path=save_path, show=False)
        generate_L3_day_plots(output_file, 'palaiseau', product, 'icon',
                              fig_type='statistic', save_path=save_path, show=False)

    output_files =[f'{root}/test_files/20210222_palaiseau_ecmwf_downsampled_cf.nc',
                   f'{root}/test_files/20210222_palaiseau_ecmwf_downsampled_iwc.nc',
                   f'{root}/test_files/20210222_palaiseau_ecmwf_downsampled_lwc.nc']
    
    for product, output_file in zip(['cf', 'iwc', 'lwc'], output_files):
        generate_L3_day_plots(output_file, 'palaiseau', product, 'ecmwf',
                              fig_type='pair', save_path=save_path, show=False)
        generate_L3_day_plots(output_file, 'palaiseau', product, 'ecmwf',
                              fig_type='statistic', save_path=save_path, show=False)
    
    output_files =[f'{root}/test_files/20200501_bucharest_era5_downsampled_cf.nc',
                   f'{root}/test_files/20200501_bucharest_era5_downsampled_iwc.nc',
                   f'{root}/test_files/20200501_bucharest_era5_downsampled_lwc.nc']

    for product, output_file in zip(['cf', 'iwc', 'lwc'], output_files):
        generate_L3_day_plots(output_file, 'bucharest', product, 'era5',
                              fig_type='pair', save_path=save_path, show=False)
        generate_L3_day_plots(output_file, 'bucharest', product, 'era5',
                              fig_type='statistic',save_path=save_path, show=False)
    """
    output_files = [f'{root}/test_files/20200501_bucharest_ecmwf_downsampled_cf.nc',
                    f'{root}/test_files/20200501_bucharest_ecmwf_downsampled_iwc.nc',
                    f'{root}/test_files/20200501_bucharest_ecmwf_downsampled_lwc.nc']

    for product, output_file in zip(['cf', 'iwc', 'lwc'], output_files):
        generate_L3_day_plots(output_file, 'bucharest', product, 'ecmwf',
                              fig_type='pair', save_path=save_path, show=False)
        generate_L3_day_plots(output_file, 'bucharest', product, 'ecmwf',
                              fig_type='statistic', save_path=save_path, show=False)


if __name__ == "__main__":
    main()
