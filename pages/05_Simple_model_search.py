import streamlit as st
import pandas as pd
from top2vec import Top2Vec

from transformers import pipeline

if 'summariser' not in st.session_state:
    st.session_state['summariser'] = False
#else:
#    st.session_state.summariser = summariser

#summariser = pipeline('summarization')
#st.session_state.summariser = summariser

# sshleifer/distilbart-cnn-12-6
def summarise(text):
    #try:
    summary_not_greed = summariser(text, max_length = 120, min_length = 20, do_sample = True)
    output = summary_not_greed[0]['summary_text']

    #except:
    #output = 'Failed to summarise'

    return output

def Convert(string):
    li = list(string.split(" "))
    return li

def find_docs_using_keyword(keywords, orig_df):
    documents, document_scores, document_ids = top2vec_model.search_documents_by_keywords(keywords=keywords, num_docs=10)
    count = 1
    for doc, score, doc_id in zip(documents, document_scores, document_ids):
        st.write(f"Result number: {count}")
        st.write(f"Document id in dataframe: {doc_id}, Score: {score}")
        st.write('Title')
        st.write(orig_df['Title'][doc_id])
        st.write('Text body')
        st.write(orig_df['Text'][doc_id])
        st.write('Summary')
        count +=1

        if 'skip due to length' in orig_df['Text'][doc_id].lower():
            st.write('Failed to summarize')
        else:
            st.write(summarise(orig_df['Text'][doc_id]))


        st.write("-----------")
        st.write()


if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:
    #st.session_state.top2vec_model = False

    st.write('Please run Top2Vec model first before looking at this page')

else:
    top2vec_model = st.session_state.top2vec_model
    df_working = st.session_state['df_working']

    st.header('Input keyword and get out first 10 documents most similar to keyword')
    #st.write(' Enter keyword(s) to find related documents')
    #st.write(" An error might occur if the keywords doesn't occur in any text")

    if 'keywords_' not in st.session_state:
        st.session_state.keywords_ = False

    keywords_ = st.text_input('Find documents with keywords')#.to_list()
    proceed_button_t2v =  st.button('Search for documents similar to keyword')

    if proceed_button_t2v:

        if st.session_state['summariser'] == False:
            st.write('Loading summarisation model')
            summariser = pipeline('summarization')
            st.session_state.summariser = summariser
            st.write('Summarisation model loaded successfully')

        else:
            summariser = st.session_state.summariser


        st.session_state.keywords_ = keywords_

    #if 'proceed_button_t2v_2' not in st.session_state:
    #    st.session_state.proceed_button_t2v_2 = False

    #keyword_button = st.button(" Proceed")
    #if proceed_button_t2v_2 :

        with st.spinner(text="In progress... This can take a few minutes"):
            find_docs_using_keyword(Convert(keywords_),df_working)

        st.write('Done')
