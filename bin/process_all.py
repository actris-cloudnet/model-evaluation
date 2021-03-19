import os
from pathlib import Path
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import configparser
<<<<<<< HEAD
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

=======
=======
import configparser
>>>>>>> 122b8aa... Fixes process_all script and bug in standard product downsampling
from model_evaluation.products.product_resampling import process_observation_resample2model
=======
from model_evaluation.products.product_resampling import resample_observation2model
>>>>>>> a109d5e... Testcase processing setup ready
from model_evaluation.plotting.plotting import generate_quick_plot, generate_single_plot
=======
from model_evaluation.products.product_resampling import process_observation_resample2model
<<<<<<< HEAD
from model_evaluation.plotting.plotting import generate_day_figures, generate_single_plot
>>>>>>> 8deb5b8... Plotting cycles and no cycles functioning
=======
from model_evaluation.plotting.plotting import generate_day_group_plots, generate_day_plot_pairs
>>>>>>> 19dc204... Plotting cycles and no cycles functioning

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    """Example processing of product downsampling system including visualization process"""
    root = os.path.split(Path(__file__).parent)[0]
    #root = os.path.split(root)[0]
    fname = f'{root}/test_files/20201208_juelich_icon-iglo-12-23.nc'
    fname2 = f'{root}/test_files/20201208_juelich_icon-iglo-24-35.nc'
    fname3 = f'{root}/test_files/20201208_juelich_icon-iglo-36-47.nc'
    cf_input = f'{root}/test_files/20201208_juelich_categorize.nc'
    cf_output = f'{root}/processed_files/test_input_icon_cf.nc'
    iwc_input = f'{root}/test_files/iwc.nc'
    iwc_output = f'{root}/processed_files/test_input_ecmwf_iwc.nc'
    lwc_input = f'{root}/test_files/lwc.nc'
    lwc_output = f'{root}/test_files/test_input_ecmwf_lwc.nc'
    input_files = [cf_input, iwc_input, lwc_input]
    output_files = [cf_output, iwc_output, lwc_output]
    save_path = f'{root}/plots/'

    for product, product_file, output_file in zip(['iwc'], [iwc_input], [iwc_output]):
        #process_observation_resample2model('icon', product, [fname, fname2, fname3], product_file, output_file)
        generate_day_group_plots(output_file, 'Mace-Head', product, 'ecmwf', save_path=save_path)
        #generate_day_plot_pairs(output_file, product, 'juelich', 'icon', save_path=save_path)
        """
        if product == 'cf':
            generate_plot_pairs(output_file, product, f'{product}_V_ecmwf', 'ecmwf', save_path=save_path)
            generate_plot_pairs(output_file, product, f'{product}_V_adv_ecmwf', 'ecmwf', save_path=save_path)
        else:
            generate_plot_pairs(output_file, product, f'{product}_ecmwf', 'ecmwf', save_path=save_path)
            generate_plot_pairs(output_file, product, f'{product}_adv_ecmwf', 'ecmwf', save_path=save_path)
        """


if __name__ == "__main__":
    main()
>>>>>>> 4f8ca63... Testcase processing setup ready
