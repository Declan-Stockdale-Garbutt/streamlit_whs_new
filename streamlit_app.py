import streamlit as st


# config page - should be able tor rename page on sidebar
st.set_page_config(
    page_title="Main Page"
)

# wreite title
st.write("# Centre for Work Health and Safety - NSW")

# write info about app
st.markdown(
    """
    #
    ### This app is built as part of the iLabs2 subject for the UTS MDSI program

    ###
    ### Functionality
    - A simple and a complex topic model are utilized to gain insights into the underlying topics over a range of documents
    - The simple model utilises a Top2Vec which is relatively fast to train but has limited functionality
    - The complex model utilizes a natural language model (Bert) to generate topics and has additional high level visualisations built in. It takes sgnificantly longer to train on documents
    - Almost all outputs including displayed dataframes, tables and visualisations can be named and downloaded for later used
    - Both simple and complex models can be downloaded and uploaded to compare models


    ### How to use
    There are a few entry points to this app
    - The first is using a text input document from Pubmed which is then converted into a json file which can be downloaded
    - Another is to load the newsapi dataframe which pulls data from Elastic Search and converts it to a json
    - A third option is to upload pdfs which are parsed and converted to json files
    - The resulting outputs from the three previous steps can be merged together into one file and used as a single json file

    ### Supported input files
    - Output from PubMed searches can be loaded into the app. Other academic sources may also be included at a later stage
    - Multiple pdfs can be loaded into this app. They will be read and parsed. They will be separated into 250 word chunks.
    - News articles loaded into Elastic Search are also input. There is no need to input any files using this process

    ### Authors
    - Declan Stockdale
    - Odette Patrick
    - Shivanand Iyer Sundaram
    - Anna Ly
"""
)
