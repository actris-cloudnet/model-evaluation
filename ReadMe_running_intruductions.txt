Running Model_evaluation software.

For software to work, user need to upload CloudnetPy and netCDF4 to used python environment.

(Installation instruction CloudnetPy: pip3 install cloudnetpy)
(Installation instruction netCDF4: pip install netCDF4)

Running is done with testing_generate_regrid_product.py located in /model_evaluation/bin/
Files for testing use is located in /model_evaluation/test_files/
ECMWF files are not at same date, idea was to check functionalities of file writing with cycles files.
So for cycles, data is incorrect.


Processing code at this stage, "generate_regrid_producst" is called.
It process one model type and one product type at once, but it process multiple model files with one call.
End product is .nc file which include one model type but all model cycles for one product.
Model files are given process in list, even if one. 

With current state processing can do with three products: iwc, lwc, cv
Files of observation data is processed with CloudnetPy and is would at directory as model files.
For running process, change path to observation files in level3.ini.

Some visualization is done within to check data. Proper plotting tools not done yet.

For all product some ready process test_files also in /test_files/ directory.

Some changes will be done to code:
- Cutting off unused model data levels
- Proper masking to model data
- Evolving model metadata
- Processing is quite slow, checking that
