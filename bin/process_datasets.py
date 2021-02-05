import os
from pathlib import Path
import configparser
import datetime
from model_evaluation.products.product_resampling import process_observation_resample2model
from model_evaluation.plotting.plotting import generate_day_group_plots

ROOT_PATH = os.path.split(Path(__file__).parent)[0]
PROCESS_CONF = configparser.ConfigParser()
PROCESS_CONF.optionxform = str
PROCESS_CONF.read(os.path.join(os.getcwd(), 'config.ini'))


def remove_missing_days(obs_files, model_files):
    for i in range(len(obs_files)):
        o_name = obs_files[i].split('/')[-1]
        o_date = [a for a in o_name.split('_') if a.isdigit()]
        o_date = datetime.datetime.strptime(o_date[0], '%Y%m%d')

        m_name = model_files[i].split('/')[-1]
        m_date = [a for a in m_name.split('_') if a.isdigit()]
        m_date = datetime.datetime.strptime(m_date[0], '%Y%m%d')
        if o_date > m_date:
            j = i
            while o_date > m_date:
                model_files.remove(model_files[j])
                j = +1
                m_date = m_date + datetime.timedelta(days=1)


def generate_casetime_list():
    dates = []
    dateFrom = PROCESS_CONF['run2']['start_date']
    dateTo = PROCESS_CONF['run2']['end_date']
    df = datetime.datetime.strptime(dateFrom, '%Y%m%d')
    dt = datetime.datetime.strptime(dateTo, '%Y%m%d')
    dates.append(dateFrom)
    while df < dt:
        df = df + datetime.timedelta(days=1)
        dates.append(df.strftime("%Y%m%d"))
    return dates


def main():
    site = PROCESS_CONF['run2']['site']
    models = PROCESS_CONF['run2']['model']
    models = [x.strip() for x in models.split(',')]

    save_plots = f'{ROOT_PATH}/plots/'
    path1 = f'{ROOT_PATH}/test_files/'
    save_files = f'{ROOT_PATH}/processed_files/'
    test_files = [os.path.join(path1, i) for i in os.listdir(path1)]
    test_files.sort()

    case_dates = generate_casetime_list()
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
                #generate_day_group_plots(save_name, site, product, model, save_path=save_plots)


if __name__ == "__main__":
    main()
