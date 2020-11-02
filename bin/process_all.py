import os
from pathlib import Path
import configparser
import datetime
from model_evaluation.products.product_resampling import process_observation_resample2model


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
    remove_missing_days(cat_files, model_files)

    for product, product_files in zip(['iwc', 'lwc', 'cf'], [iwc_files, lwc_files, cat_files]):
        for i in range(len(product_files)):
            f_name = product_files[i].split('/')[-1]
            date = [a for a in f_name.split('_') if a.isdigit()]
            save_name = os.path.join(save_path, f"{date[0]}_{model}_{product}_regrid.nc")
            process_observation_resample2model(
                model, product, [model_files[i]], product_files[i], save_name)

            print(f"Done Processing file {product_files[i]}")
        print(f"Done Processing product {product}")
    print("Done Processing set")
print("Full processing done")

