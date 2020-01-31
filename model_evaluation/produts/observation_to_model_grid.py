"""
Gets: product from level 2a/cat-file and model witch will be used for griding.

Model file at this point is probably including only one grid point witch represents
the sites location. Selecting correct grid point will be chosen in other file. Depend on
the state of model files.


"""

import numpy as np
import netCDF4


def generate_data2modelgrid(cnet_data, model_data):
    print("lol")
    "Tähän perus gridauksen prosessointi"
