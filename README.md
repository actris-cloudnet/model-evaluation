# Model evaluation

ACTRIS Cloudnet Model evaluation software is an application to reprocess CloudnetPy products with statistical analysis to Level3 products. 
Model evaluation software compares observations of clouds and properties to simulated ones and creates statistical analysis and visualization for multible weather models.

Current under developing version of model evaluation processes day scale downsampled products with visualizations.


### From the source
```
$ git clone https://github.com/actris-cloudnet/model_evaluation
$ cd model_evaluation/
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python3 -m pip install .
(venv) $ python3 bin/process_all.py
```

Running an example process will take some time so don't get nervous unless run takes over 1 minute :) 