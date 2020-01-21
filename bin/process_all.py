""" This file will include all basic functionality for processing model evaluation.

1) Select product(s) (of level 2a) to be evaluated

2) Collect data of product(s) for given site
   - Maybe all sites are processed in order, not at same time

3) Get model data for given model
    - Model data file might all ready have only one grid point.
    if not, create method for selecting the closest data of observation location

4) Modify level 2a data to same grid as model grid (time, height)
    - Is time resolution always same (1h) regardless of the model?
    The real time resolution of the models?

Level 2b product(s) done. Data might be saved at this point

5) Calculate statistics for product(s)
    - So many thing is still unclear here

6) ? Save statistics somewhere
    - It might be enough to just calculate stuff. It depends of processing
    - Includes multiple different type of statistics. Maybe option is good to have

7) Visualization of statistics

Model evaluation done
"""
