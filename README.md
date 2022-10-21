# WHS Streamlit Application
This application was developed as part of the iLabs 2 subject

## Running the application




### Locally
The files can be downloaded locally either into the root directory or into a virtual environment. 
## Prerequisities

Before you begin, ensure you have met the following requirements:

* You have a _Windows/Linux/Mac_ machine running [Python 3.8+](https://www.python.org/).
* You have installed the latest versions of [`pip`](https://pip.pypa.io/en/stable/installing/) or `conda` ([Anaconda](https://www.anaconda.com/distribution/)).


**Instructions for `conda`**

```bash
# Create virtual environment click y to install additional downloads if required
$ conda create -n streamlit_whs_new python=3.8

# Activate the virtual environment:
$ conda activate streamlit_whs_new

# clone directory into virtual environment
(streamlit_whs_new)$ git clone https://github.com/Declan-Stockdale/streamlit_whs_new.git

# move into virtual environment directory
$ cd streamlit_whs_new

# install required python packages
(streamlit_whs_new)$ pip install -r requirements.txt

# If error for failed building wheel for hdbscan run the following then repeat previous line
(streamlit_whs_new)$ conda install -c conda-forge hdbscan

# Run the app
(streamlit_whs_new)$ streamlit streamlit_app.py

# To deactivate (when you're done):
(streamlit_whs_new)$ conda deactivate
```



### Online
The app has been deloyed in the streamlit app here https://declan-stockdale-streamlit-whs-new-streamlit-app-muwg9c.streamlitapp.com
It is fully functional online however it takes additional time to load pages and run certain functionalities of the app.

