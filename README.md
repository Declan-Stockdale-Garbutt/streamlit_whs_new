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

To access the app later without re-installing it

```bash
# Activate the environment
$conda activate streamlit_whs_new

# navigate inside the directory
(streamlit_whs_new)$cd streamlit_whs_new

# run app
(streamlit_whs_new)$streamlit run streamlit_app.py

# To deactivate (when you're done):
(streamlit_whs_new)$ conda deactivate
```


### Online
The app has been deloyed in the streamlit cloud here https://declan-stockdale-streamlit-whs-new-streamlit-app-muwg9c.streamlitapp.com
It is fully functional online however it takes additional time to load pages and run certain functionalities of the app.

## Functionality
This application has numerous functionalities and entry points. Some pages require previous pages to function correctly. If so, instructions on how to proceed will be displayed.

### Streamlit app
This is the main page of the application and details various functioanlites and how to use the app

![Screenshot (84)](https://user-images.githubusercontent.com/53500810/206886292-393bf2d5-cf49-4c73-9bad-80c0cc76e417.png)


### Convert Elastic to Json
This pulls data directly from a Elastic Search database which has been rpe populated with various academic and news sources such as Education Resources Information Center (ERIC) and New York Times. All necessary processing occurs and a json file can be downloaded. This may not work due to dependecy errors.

![image](https://user-images.githubusercontent.com/53500810/206886441-36cf6473-d8c1-4b5b-9c53-8213b85e3452.png)


### Convert pdf to json
This page allows for multiple pdf files to be uploaded and parsed at once. It is assumed that the uploaded files will be multipage files with alot of text data. Some of the natral language models used for alter analysis have troulbe with large text data so the approach taken was to chunk the files up into segments of 250 words. There is no check to determine whether the chunks end mid sentence, this will be investigated in future. 

![image](https://user-images.githubusercontent.com/53500810/206886567-a00a3f8d-a4c1-4320-af1c-659c12aeb4e4.png)


The resulting dataframe file contains the data along with a chunk name if a source was chunked e.g. source1_chunk1, source1_chunk2 etc. The dataframe should be downloaded as a json

![image](https://user-images.githubusercontent.com/53500810/206886629-794329bf-18ac-4b71-9e5e-92a6cf4c2679.png)

### Convert Pudmed Text to json
This assumes the user has followed the steps required to download abstracts from PubMed, if not they are displayed in the page regardless

![image](https://user-images.githubusercontent.com/53500810/206886656-b3921ca3-042e-45e2-90d9-e5270cb6e3af.png)


### Merge multiple json
Allows to merge the results from previous pages. 

![image](https://user-images.githubusercontent.com/53500810/206886695-84b4ab13-003c-48c7-9c64-5271ff5ad933.png)


### Load json
Upload a json file. Should be used after using a previous page to generate a jso file in the correct format. Uploading to the first option allows for various processing steps to occur such as remove stopwords, lemmatization and remoe punctuation. Use the lower option is json is already clean.

![image](https://user-images.githubusercontent.com/53500810/206886716-9cf360b8-2a93-4579-81ba-787dadbf10de.png)

![image](https://user-images.githubusercontent.com/53500810/206886755-850f8e18-4efd-4770-994a-05f1be35bd43.png)

### Basic Keyword Analysis
A json must be uploaded for this page to proceed. If an error is shown, please click the button and it will disappear. This is a known bug.

Keyword extraction will occur using KeyBERT algorithm 

### Top2Vec model document similarity


### Top2Vec wordclouds


### Top2Vec search documents



### Top2Vec search similar keywords


### Top2Vec keyword frequency analysis


### BERTopic (language model)


### BERTopic similar keywords


### BERTopic keyword frequency analysis


### Work in progress


### Bugs and issues




