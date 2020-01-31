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
