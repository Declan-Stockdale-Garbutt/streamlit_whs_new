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

Keyword extraction will occur using KeyBERT algorithm. This can take a long time

Outputs include most frequent words across data (title and text)
![image](https://user-images.githubusercontent.com/53500810/206887073-ecb9500b-0f49-4820-ba65-389fdcb57afa.png)

Also includes interactive table of most frequent words for each year in the uploaded file
![image](https://user-images.githubusercontent.com/53500810/206887107-a44fc25c-0a33-4952-83fb-1d18b900af79.png)



### Top2Vec model 
This is where the Top2Vec model is created using the uploaded json file. A new model can be createdor alternatively a previously created model can be uploaded.
Training a model can taks some time. Each document is assigned to a topic.

The results are the number of documents within each topic as well as interactive tables howing the documents within each topic


![image](https://user-images.githubusercontent.com/53500810/206887156-5c83509e-05a5-4999-bf35-bc6cd27167f7.png)

![image](https://user-images.githubusercontent.com/53500810/206887323-feb52a94-f39b-4dd9-ace4-9378d5b6f17c.png)




### Top2Vec wordclouds
Generate word cloubds for each topic discoverd

![image](https://user-images.githubusercontent.com/53500810/206887276-8adef1c9-8ce3-4421-a00b-f167be15ca12.png)


### Top2Vec search documents
This page allows for the user to input a keyword e.g. exercise and the top 10 documents associated with that word will be returned along with a ~100 word summary.
It can take a long time on the first use as it must load the sumamrisation model which can take some time.


![image](https://user-images.githubusercontent.com/53500810/206887400-d4789298-10ad-4097-9887-5ec8e63a4c1d.png)



### Top2Vec search similar keywords
Enter a keyword and find similar keywords. This can be used to expand searches to find new sources.

![image](https://user-images.githubusercontent.com/53500810/206887429-e57cb656-0d29-4dbc-8e5e-88419a7f808f.png)


### Top2Vec keyword frequency analysis
Using the keywords extracted using KeyBERT and topic assignment of Top2Vec model for each document, the keywords within each topic are displayed in an interactive table for both topic and year

![image](https://user-images.githubusercontent.com/53500810/206887511-f0800d02-7dce-4231-8b03-5862c0f58d55.png)


### BERTopic (language model)
This is where the BERTopic model is created using the uploaded json file. A new model can be createdor alternatively a previously created model can be uploaded.
Training a model can takes some time. 

There is a known bug where uploading a previously cleaned file results in an error in the Load json page. This can be remedied by uploading the file as if it was new and not selecting any additional cleaning options.

![image](https://user-images.githubusercontent.com/53500810/206887540-0b11482a-954f-479f-a63a-797286817b48.png)

The model assigns each document to a topic. The results of the page initially include a table of documents for each topic along with various visuals shown below. The visuals themselves take a while to load.

![image](https://user-images.githubusercontent.com/53500810/206887953-cfbc8a9c-a6ad-4fb4-a153-33fdacddd923.png)

#### Visual document embeddings
The figure shows the proximity of topics and the underlying documents. This can be used to gain insight into what topics are similar to others. 

![image](https://user-images.githubusercontent.com/53500810/206888080-7178cb40-2d00-49bf-acad-d7a63933c9da.png)

#### Heatmap of topics
This shows a correlation matrix of how all how much all topics are related. A darker square incdicates more related, whereas a light square indicates less relatedness.

#### Hierarchial Tree diagram

![image](https://user-images.githubusercontent.com/53500810/206888121-89fd3002-79f3-4d71-b8ad-579b75147f41.png)


![image](https://user-images.githubusercontent.com/53500810/206888107-792f6e6c-7cb4-425d-a032-b6ff0bbe5870.png)


#### Barchart
Top 10 words for each topic fro BERTopic model
![image](https://user-images.githubusercontent.com/53500810/206888144-88466846-232a-4694-8a49-d8022008eaf4.png)

#### Topics over time
This shows how the frequency of each topic changes over time. The timestamps used are the year values within the inital cleaned dataframe. It is interactive and topics can be removed or selected by clicking the topic of interest on the right

![image](https://user-images.githubusercontent.com/53500810/206888182-ed0b06b8-19b0-4b48-a48a-2b54b7aaee7a.png)


### BERTopic similar keywords
The result of this page is a table of topics and keywords which are most similar to the input keyword.

![image](https://user-images.githubusercontent.com/53500810/206888215-18a13ebb-2e32-421b-9f31-39d04bf7a86e.png)


### BERTopic keyword frequency analysis
The result of the generated topics for each document and combined with the keyword analysis output

An interactive table for each topic is created showing the frequency of keywords over time.

![image](https://user-images.githubusercontent.com/53500810/206888230-5c79544c-9107-49ff-9236-df4b3dd03515.png)


### Work in progress
Had functionality to implemetn PyLDAVis but due to dependency issue it was removed. This is a place holder while work arounds are explored

### Bugs and issues
Describes various bugs and issues associated with the app. If you find additional bugs not mentioned, please contact the authors or submit a pull request



