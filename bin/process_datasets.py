import os
from pathlib import Path
import configparser
from collections import Counter
from model_evaluation.products.product_resampling import process_observation_resample2model
from model_evaluation.plotting.plotting import generate_L3_day_plots

ROOT_PATH = os.path.split(Path(__file__).parent)[0]
PROCESS_CONF = configparser.ConfigParser()
PROCESS_CONF.optionxform = str
PROCESS_CONF.read(os.path.join(os.getcwd(), 'config.ini'))


def split_files_to_dates(test_files, case):
    dates = []
    test_files = [test_files[i].split('/')[-1] for i in range(len(test_files))]
    test_files = [test_files[i].split('_')[0] for i in range(len(test_files))]
    C = Counter(test_files)
    test_files = [[k, ]*v for k, v in C.items()]
    min_n_files = PROCESS_CONF[case]['min_files']
    for cases in test_files:
        if len(cases) >= min_n_files:
            dates.append(cases[0])
    return dates


# For running this, loading some testfiles is required!
def main():
    save_plots = f'{ROOT_PATH}/plots/'
    path = os.path.split(ROOT_PATH)[0]
    cases = PROCESS_CONF.sections()
    for case in cases:

        test_case_files = f'{path}/model_evaluation_test_files/{case}/'
        save_files = f'{path}/model_evaluation_processed_files/{case}'
        site = PROCESS_CONF[case]['site']
        models = PROCESS_CONF[case]['model']
        models = [x.strip() for x in models.split(',')]

        test_files = [os.path.join(test_case_files, i) for i in os.listdir(test_case_files)]
        test_files.sort()
        case_dates = split_files_to_dates(test_files)
        test_files = [f for f in test_files for date in case_dates if date in f and site in f]

        for model in models:
            model_file_set = [[f for f in test_files if model in f and date in f] for date in case_dates]
            cat_files = [f for f in test_files if 'categorize' in f]
            iwc_files = [f for f in test_files if 'iwc' in f]
            lwc_files = [f for f in test_files if 'lwc' in f]

            for product, product_files in (zip(['iwc', 'lwc', 'cf'], [iwc_files, lwc_files, cat_files])):
                for i in range(len(product_files)):
                    f_name = product_files[i].split('/')[-1]
                    date = [a for a in f_name.split('_') if a.isdigit()]
                    save_name = os.path.join(save_files, f"{date[0]}_{site}_{model}_downsampled_{product}.nc")
                    process_observation_resample2model(
                        model, product, model_file_set[i], product_files[i], save_name)
                    generate_L3_day_plots(save_name, product, site, model, save_path=save_plots)


if __name__ == "__main__":
    main()
