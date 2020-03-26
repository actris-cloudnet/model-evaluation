"""
This module calculates cloud fraction for both observated and simulated data.
"""
from cloudnetpy.products.product_tools import ProductClassification


def generate_cv(data_obj, data_file):
    class_obj = ProductClassification(data_file)
