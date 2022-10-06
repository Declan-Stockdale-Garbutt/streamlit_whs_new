import streamlit as st

# Entry point

st.set_page_config(
    page_title="Main Page"
)

st.write("# Centre for Work Health and Safety - NSW")
#st.sidebar.success("Select a page")

st.markdown(
    """
    ### This app is built as part of the iLabs2 subject for the UTS MDSI program

    ###
    ### Functionality
    - A simple and a complex topic model are utilized to gain insights into the topics over a range of documents
    - The simple model utilises a Top2Vec which is quick to run but has limited functionality
    - The complex model utilizes a natural lange model (Bert) to generate topics and has additional high level visualisations built in


    ### How to use
    There are two entry points to this app
    - The first is using a text input document from Pubmed which is then converted into a json file which can be downloaded
    - The second is to upload a json file, using the output of the previous step or finding a json from another source that matches the structure

    ### Supported documents
    - Currently only results from Pubmed searches are supported, this will be updated shortly
    - Any document that can have the attributes (Title, Text, Published year) can be used in this model
    - The additional columns will be filled with 'unknown' if they are not included
    - In the case of research articles, PMID or DOI is unique, for other documents a univeral unique identifier will need to be generated

    ### Authors
    - Declan Stockdale
    - Odette Patrick
    - Shivanand Iyer Sundaram
    - Anna Ly
"""
)
