#!/usr/bin/env python3
import sys
import subprocess
import os
from os import path
import argparse
from tempfile import TemporaryDirectory

ROOT_PATH = os.path.abspath(os.curdir)
sys.path.append(f'{ROOT_PATH}/model_evaluation/products')
process_day_evaluation = __import__("product_resampling")
SCRIPT_PATH = path.dirname(path.realpath(__file__))
test_file_model = f'{ROOT_PATH}/test_files/20190517_mace-head_ecmwf.nc'
test_file_product = f'{ROOT_PATH}/test_files/20190517_mace-head_lwc-scaled-adiabatic.nc'


def _process():
    tmp_dir = TemporaryDirectory()
    temp_file = f'{tmp_dir.name}/xx.nc'
    process_day_evaluation.process_L3_day_product('ecmwf', 'lwc',
                                                  [test_file_model],
                                                  test_file_product,
                                                  temp_file)
    try:
        subprocess.call(['pytest', '-v', f'{SCRIPT_PATH}/tests.py', '--full_path',
                         temp_file])
    except subprocess.CalledProcessError:
        raise
    tmp_dir.cleanup()


def main():
    _process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model evaluation liquid water content processing e2e test.')
    ARGS = parser.parse_args()
    main()
