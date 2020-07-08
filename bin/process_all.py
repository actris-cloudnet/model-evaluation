""" This file will include all basic functionality for processing model evaluation.

1) Initialized wanted sites to be evaluated from config(?)
    - Listed all models which have data for site
    - All level 1 and 2 files of date will be generated unless mention otherwise
    - As default all listed observation data types will be generated to L3, unless
    mention otherwise

2) Collect data of product(s) for given site
    - Now test data will be loaded local dir, later from server
    - Maybe all sites are processed in order, not at same time
    - Basically define path to files

3) Get model data for given model
    - Model data file is all ready have only one grid point
    - Read only vertical grid/height (above the sea or site level?) from data
    - Data itself is needed only in statistical state and plotting
    - As default generate all listed models unless mention otherwise

4) Modify level 1 and 2a data to same grid as model grid (time, height)
    - Model files are generated elsewhere, so regriding is done to dimension depending
    of model, not default 1 hour resolution
    - Need to select time window wisely, maybe variation between time resolution is needed?
    Lets assume 15min both side to be good option (~60 observation in averaging)
    - Read observation data in this state(?)
    - 2) and 3) are probably class inside 4)-file

    Level 2b product(s) done. Data might be saved at this point

5) Calculate L3 products from l2b and save to .nc file
    - Not at this point strong idea what is done...
    - In processing of Cloudnet there is at least Iwc, Lwc, Cloud fraction
    - TODO: Study this later on
    - Level 3 files are saved in this state as .nc files

6) Calculate statistics for product(s)
    - So many thing is still unclear here

7) ? Save statistics somewhere
    - It might be enough to just calculate stuff. It depends of processing
    - Includes multiple different type of statistics. Maybe option is good to have

8) Visualization of statistics

Model evaluation done
"""

import os
from pathlib import Path
import configparser
from model_evaluation.products.grid_product import generate_regrid_products

root_path = os.path.split(Path(__file__).parent)[0]
L3_CONF = configparser.ConfigParser()
L3_CONF.read(os.path.join(root_path, 'model_evaluation/level3.ini'))
PROCESS_CONF = configparser.ConfigParser()
PROCESS_CONF.read(os.path.join(os.getcwd(), 'config.ini'))

site = PROCESS_CONF['run']['site']
model = L3_CONF[site]['model']

path1 = '/home/korpinen/Documents/ACTRIS/test_data_files/2018_juelich'
path2 = '/home/korpinen/Documents/ACTRIS/test_data_files/2019_juelich'
files_2018 = [os.path.join(path1, i) for i in os.listdir(path1)]
files_2019 = [os.path.join(path2, i) for i in os.listdir(path2)]
files_2018.sort()
files_2019.sort()
save_path1 = '/home/korpinen/Documents/ACTRIS/test_data_files/regrid_2018_juelich/'
save_path2 = '/home/korpinen/Documents/ACTRIS/test_data_files/regrid_2019_juelich/'

for set, save_path in zip([files_2018, files_2019], [save_path1, save_path2]):
    model_files = [f for f in set if model in f]
    cat_files = [f for f in set if 'categorize' in f]
    iwc_files = [f for f in set if 'iwc' in f]
    lwc_files = [f for f in set if 'lwc' in f]

    for product, product_files in zip(['iwc', 'lwc', 'cv'], [iwc_files, lwc_files, cat_files]):
        for i in range(len(model_files)):
            f_name = product_files[i].split('/')[-1]
            date = [a for a in f_name.split('_') if a.isdigit()]
            save_name = os.path.join(save_path, f"{date[0]}_{model}_{product}_regrid.nc")
            generate_regrid_products(model, product, [model_files[i]], product_files[i], save_name)
