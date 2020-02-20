from  model_evaluation.produts.generate_modeldata import generate_model_data

# test file
fname = '/home/korpinen/Documents/ACTRIS/old_files_model_evalutation/model_files/20190517_mace-head_ecmwf.nc'
oname = '/home/korpinen/Documents/ACTRIS/model_evaluation/test_data_ecmwf.nc'

generate_model_data('ecmwf', fname, oname)