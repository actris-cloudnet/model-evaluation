# Model evaluation

ACTRIS Cloudnet Model evaluation software is an application to process CloudnetPy level 2 (L2) products to statistical analysis called level 3 (L3) products. 
Model evaluation software compares observations of clouds and properties to simulated ones from various NWP models and creates statistical analysis and visualization.

At the current under developing version of Model evaluation, the software processes L3 day scale downsampled products with an option to generate also visualizations and statistics.
Thicker observation time-height grid of L2 products is downsampled to a wider time-height grid of select model by calculating average value of observation bins inside grid-point of model.
The motive to do so is to modify L2 grid to be same size as model grid to do case analysis of day and at the later state also longer time period.

By running function ```process_L3_day_products()``` from ```product_resampling.py```, software creates netCDF-file of L3 day products. 
In the file there is downsampled L2 products with name format ```product_method_model_cycle```, model variable of product with name format ```model_cycle_product```, 
simulation run variables with a both cycle and model dependencies.


### Model evaluation Installation and Usage 
```
$ git clone https://github.com/actris-cloudnet/model-evaluation
$ cd model-evaluation/
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python3 -m pip install .
(venv) $ python3 bin/process_all.py
```
