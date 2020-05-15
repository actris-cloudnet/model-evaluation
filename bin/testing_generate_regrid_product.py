import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model_evaluation.products.grid_product import generate_regrid_products
from model_evaluation.plotting.plotting import generate_quick_plot, generate_single_plot
from cloudnetpy.plotting import generate_figure

# Path to .../model_evaluation/
root = os.path.split(Path(__file__).parent)[0]

# test files
fname = f'{root}/test_files/20190517_mace-head_ecmwf.nc'
iwc_name = f'{root}/test_files/test_data_ecmwf_iwc.nc'
lwc_name = f'{root}/test_files/test_data_ecmwf_lwc.nc'
cv_name = f'{root}/test_files/test_data_ecmwf_cv.nc'
test_f1 = f'{root}/test_files/20130909_mace-head_ecmwf-exp0001-0-11.nc'
test_f2 = f'{root}/test_files/20130909_mace-head_ecmwf-exp0001-12-23.nc'

save_path = f'{root}/plots/'
iwc_file = f'{root}/test_files/iwc.nc'
lwc_file = f'{root}/test_files/lwc.nc'

# Run all product with all test_model files
for product, oname in zip(['iwc', 'lwc', 'cv'],[iwc_name, lwc_name, cv_name]):
    generate_regrid_products('ecmwf', product, [fname, test_f1, test_f2], oname)
    generate_quick_plot(oname, product, 'ecmwf', save_path=save_path, show=False)
    #generate_single_plot(oname, product, f'{product}_obs_ecmwf', 'ecmwf')

# To compare plot CloudnetPy figs also
for product, name in zip(['iwc', 'lwc'], [iwc_file, lwc_file]):
    generate_figure(name, [product], save_path=save_path, show=False)

