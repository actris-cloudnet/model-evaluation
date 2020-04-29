import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy.ma as ma
import netCDF4
from model_evaluation.products.grid_product import generate_regrid_products
from cloudnetpy.plotting import plot_2d
from model_evaluation.plotting.plotting import generate_quick_plot

# Path to .../model_evaluation/
root = os.path.split(Path(__file__).parent)[0]

# test files
fname = f'{root}/test_files/20190517_mace-head_ecmwf.nc'
iwc_name = f'{root}/test_files/test_data_ecmwf_iwc.nc'
lwc_name = f'{root}/test_files/test_data_ecmwf_lwc.nc'
cv_name = f'{root}/test_files/test_data_ecmwf_cv.nc'
test_f1 = f'{root}/test_files/20130909_mace-head_ecmwf-exp0001-0-11.nc'
test_f2 = f'{root}/test_files/20130909_mace-head_ecmwf-exp0001-12-23.nc'

# Run all product with all test_model files
for product, oname in zip(['iwc', 'lwc', 'cv'],[iwc_name, lwc_name, cv_name]):
    #generate_regrid_products('ecmwf', product, [fname, test_f1, test_f2], oname)
    generate_quick_plot(oname, product, 'ecmwf')
    lol

"""
data1 = netCDF4.Dataset(lwc_name).variables['ecmwf_lwc'][:]
data1[data1 <= 0] = ma.masked
data2 = netCDF4.Dataset(lwc_name).variables['lwc_obs_ecmwf'][:]
time = netCDF4.Dataset(lwc_name).variables['time'][:]
height = netCDF4.Dataset(lwc_name).variables['ecmwf_height'][:]

lwc_file = '/home/korpinen/Documents/ACTRIS/cloudnet_products/tests/source_data/lwc.nc'
lwc_data = netCDF4.Dataset(lwc_file).variables['lwc'][:]
lwc_time = netCDF4.Dataset(lwc_file).variables['time'][:]
lwc_height = netCDF4.Dataset(lwc_file).variables['height'][:]

plot_2d(data1)
plot_2d(data2)
plot_2d(lwc_data)
"""