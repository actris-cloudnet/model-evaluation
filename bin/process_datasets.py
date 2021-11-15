import os
from pathlib import Path
import configparser
from collections import Counter
from model_evaluation.products.product_resampling import process_L3_day_product
from model_evaluation.plotting.plotting import generate_L3_day_plots

ROOT_PATH = os.path.split(Path(__file__).parent)[0]
PROCESS_CONF = configparser.ConfigParser()
PROCESS_CONF.optionxform = str
PROCESS_CONF.read(os.path.join(os.getcwd(), 'config.ini'))


def select_fileset_with_dates(files, case):
    start = PROCESS_CONF[case]['start_date']
    end = PROCESS_CONF[case]['end_date']
    start_indices = [files.index(f) for f in files if start in f]
    end_indices = [files.index(f) for f in files if end in f]
    try:
        return files[start_indices[0]:end_indices[-1]+1]
    except IndexError:
        return files


def find_missing_dates(test_files, case, model):
    dates = []
    test_files = [test_files[i].split('/')[-1] for i in range(len(test_files))]
    test_types = [test_files[i].split('_')[-1] for i in range(len(test_files))]
    model_files = [test_types[i] for i in range(len(test_types)) if model in test_types[i]]
    model_files = list(set(model_files))
    if len(model_files) > 1:
        for m in model_files[:-1]:
            for f in test_files:
                if m in f:
                    test_files.remove(f)
    test_files = [test_files[i].split('_')[0] for i in range(len(test_files))]
    C = Counter(test_files)
    test_files = [[k, ]*v for k, v in C.items()]
    min_n_files = PROCESS_CONF[case]['min_files']
    for cases in test_files:
        if len(cases) >= int(min_n_files):
            dates.append(cases[0])
    return dates


# For running this, loading some test files is required!
# Changing Config-files info also required!
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
        test_files = select_fileset_with_dates(test_files, case)

        for model in models:
            case_dates = find_missing_dates(test_files, case, model)
            test_files = [f for f in test_files for date in case_dates if date in f and site in f]

            model_file_set = [[f for f in test_files if model in f and date in f] for date in case_dates]
            cat_files = [f for f in test_files if 'categorize' in f]
            iwc_files = [f for f in test_files if 'iwc' in f]
            lwc_files = [f for f in test_files if 'lwc' in f]

            for product, product_files in (zip(['iwc', 'lwc', 'cf'], [iwc_files, lwc_files, cat_files])):
                for i in range(len(product_files)):
                    f_name = product_files[i].split('/')[-1]
                    date = [a for a in f_name.split('_') if a.isdigit()]
                    save_name = os.path.join(save_files, f"{date[0]}_{site}_{model}_downsampled_{product}.nc")
                    process_L3_day_product(model, product, model_file_set[i], product_files[i], save_name)
                    generate_L3_day_plots(save_name, product, model, save_path=save_plots)
                    generate_L3_day_plots(save_name, product, model, fig_type='statistic',
                                          save_path=save_plots)


if __name__ == "__main__":
    main()
