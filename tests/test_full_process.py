import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model_evaluation.products.product_resampling import resample_observation2model
import requests
import importlib

PROCESS = True
MODEL = 'ecmwf'


def _load_test_data(input_path):
    url = 'http://devcloudnet.fmi.fi/files/cloudnetpy_test_input_files.zip'
    zip_name = os.path.split(url)[-1]


def _process_product_file(product_type, path, source_file):
    resample_observation2model()
    output_file = f"{path}{product_type}.nc"
    return (output_file)


def main():
    test_path = Path(__file__).parent[0]
    source_path = f"{test_path}/test_files/"
    _load_test_data(source_path)

    product_file_types = ['cf', 'iwc', 'lwc']
    for file in product_file_types:
        # poimitaan source file source_pathista
        _process_product_file(file, source_path, source_file='')
        # poimi luotu filu... tai luo koko homma temp-fileeseen?
        # TEstaa meta läpi


if __name__ == "__main__":
    main()
