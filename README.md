# WHS Streamlit Application
This application was developed as part of the iLabs 2 subject

## Running the application




### Locally
The files can be downloaded locally either into the root directory or into a virtual environment. 
## Prerequisities

Before you begin, ensure you have met the following requirements:

* You have a _Windows/Linux/Mac_ machine running [Python 3.6+](https://www.python.org/).
* You have installed the latest versions of [`pip`](https://pip.pypa.io/en/stable/installing/) and [`virtualenv`](https://virtualenv.pypa.io/en/stable/installation/) or `conda` ([Anaconda](https://www.anaconda.com/distribution/)).


**Using `conda`**

```bash
$ conda create -n streamlit_whs python=3.8

# Activate the virtual environment:
$ conda activate streamlit_whs

# To deactivate (when you're done):
(streamlit_whs)$ conda deactivate
```

**Using `virtualenv`**

```bash
$ virtualenv streamlit_whs --python=python3

# Activate the virtual environment:
$ source streamlit_whs/bin/activate

# To deactivate (when you're done):
(streamlit_whs)$ deactivate
```


To install the requirements using `pip`, once the virtual environment is active:
```bash
(streamlit_whs)$ pip install -r requirements.txt
```


#### Running the script
Finally, if you want to run the main script:
```bash
(streamlit_whs)$ streamlit streamlit_app.py
```


### Online
The app has been deloyed in the streamlit app here https://declan-stockdale-streamlit-whs-new-streamlit-app-muwg9c.streamlitapp.com
It is fully functional online however it takes additional time to load pages and run certain functionalities of the app.

