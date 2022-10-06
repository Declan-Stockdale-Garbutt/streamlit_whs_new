import streamlit as st
from bertopic import BERTopic
#from sentence_transformers import SentenceTransformer
#from bertopic import BERTopic
from umap import UMAP
import pandas as pd

st.header('Search through complex model for similar words')

if "df_working" not in st.session_state:
    st.write('Please upload a json file in previous page before proceeding with Berttopic modelling')

if 'berttopic_model' not in st.session_state:
    st.write('Please run the previous page to generate a model')

else:
    berttopic_model = st.session_state.berttopic_model

    if 'keywords_bert' not in st.session_state:
        st.session_state.keywords_bert = False

    keywords_bert = st.text_input('Find documents with keywords')#.to_list()
    proceed_button_bert =  st.button('Search for documents containing keyword')

    if proceed_button_bert:

        associated_topics_keyword = pd.DataFrame()

        for topic_id in berttopic_model.find_topics(keywords_bert)[0]:
            topic_word_list = []

            word = berttopic_model.get_topic(topic=topic_id)

            for word_val in word:
                topic_word_list.append(word_val[0])

            topic_word_df = pd.Series(topic_word_list,name = topic_id)
            associated_topics_keyword = pd.concat([associated_topics_keyword,topic_word_df],axis = 1)

        st.write('Table of topics and associated words for a given keyword')
        st.write(associated_topics_keyword)
