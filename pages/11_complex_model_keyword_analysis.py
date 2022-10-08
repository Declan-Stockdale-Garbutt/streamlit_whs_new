import streamlit as st
from keybert import KeyBERT
from textblob import TextBlob
import pandas as pd
from nltk.corpus import stopwords
#import texthero as hero
stop = stopwords.words('english')
pd.set_option('precision', 0)
#from sklearn.feature_extraction.text import TfidfVectorizer


st.header('Use keyword extractor to find most common keywords for each year using complex model')

if "df_working" not in st.session_state:
    st.write('Please upload a json file in previous page before proceeding with Berttopic modelling')
else:
    #check that keybert has alrady been performed
    if 'keywords_df' not in st.session_state:
        st.write('Please run Basic keyword analysis to generate keywords then return to this page')
    elif 'berttopic_model_df' not in st.session_state:
        st.write('Please run complex model to assign topics for each document then return to this page')
    else:
        df_working = st.session_state.df_working
        final_t2v_df = st.session_state.berttopic_model_df # just changed this value

        st.write('df with keywords')
        st.write(df_working)

        st.write('initial bert df')
        st.write(final_t2v_df)


        # sort dataframes by Title column
        final_t2v_df = final_t2v_df.sort_values(by=['Title'])
        final_t2v_df = final_t2v_df.reset_index( drop=True)
        #st.write(final_t2v_df)
        final_t2v_df = final_t2v_df[['bert_topic_id']]#.drop(columns=['Title','bert_probability'],axis =1 )
        st.write('after drop bert df bert df')
        st.write(final_t2v_df)

        df_working = df_working.sort_values(by=['Title'])
        df_working = df_working.reset_index(drop=True)

        final_df_t2v = pd.concat([df_working,final_t2v_df],axis = 1)

        # ready to model

        st.subheader(' Simple model keyword analysis')
        view_simple_model_button = st.button('View keywords on simple model',key = "view_simple_model_button")

        #if 'view_simple_model_button' not in st.session_state:

        st.write('look at df')
        st.write(final_df_t2v)
        if view_simple_model_button:
            st.dataframe(final_df_t2v)

            close_view_df_year = st.button('Close view')
            if close_view_df_year:
                view_simple_model_button = False




        st.subheader('Find occurences of Texblob keywords by topic id over time')
        if 'topic_slider_val' not in st.session_state:
            st.session_state.topic_slider_val = False

        topic_slider_val = st.select_slider('Choose a topic id ', options = sorted(final_df_t2v['bert_topic_id'].unique()))
        st.session_state.topic_slider_val = topic_slider_val


        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        topic_keyword_year_df = pd.DataFrame()
        for year in proper_cols_:

            #st.write('type year')
            #st.write(type(year)) #str
            #st.write('type of year')
            #st.write(type(final_df_t2v['Year']))
            #st.write('type of topic')
            #st.write(type(final_df_t2v['bert_topic_id']))



            temp_year_df_topic = final_df_t2v[(final_df_t2v['Year'] == (year)) & (final_df_t2v['bert_topic_id'] == (topic_slider_val))]
            #st.write('temp_year_df_topic', temp_year_df_topic)
            '''
            temp_year_df_topic = pd.Series(' '.join(temp_year_df_topic['textblob_nouns']).lower().split(), name = str(year)).value_counts()
            topic_keyword_year_df = pd.concat([topic_keyword_year_df,temp_year_df_topic],axis = 1)
            '''
        #st.write('Keyword frequency per year and topic')
            #st.write('year',year),
        st.write(f" Showing top keywords for topic id {topic_slider_val}")
        #topic_keyword_year_df
        topic_keyword_year_df = topic_keyword_year_df.fillna(0)
        topic_keyword_year_df = topic_keyword_year_df.astype(int)

        st.dataframe(topic_keyword_year_df.fillna(0))

###################
# adding Keybert
        st.subheader('Find occurences of Bert keywords by topic id over time')
        if 'topic_slider_val' not in st.session_state:
            st.session_state.topic_slider_val = False

        topic_slider_val = st.select_slider('Choose a topic id ', options = sorted(final_df_t2v['bert_topic_id'].unique()),key = 'bert_topic_slider')
        st.session_state.topic_slider_val = topic_slider_val


        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        topic_keyword_year_df = pd.DataFrame()
        for year in proper_cols_:
            temp_year_df_topic = final_df_t2v[(final_df_t2v['Year'] == str(year)) & (final_df_t2v['bert_topic_id'] == (topic_slider_val))]
            #st.write('temp_year_df_topic', temp_year_df_topic)

            temp_year_df_topic = pd.Series(' '.join(temp_year_df_topic['keywords_bert']).lower().split(), name = str(year)).value_counts()
            topic_keyword_year_df = pd.concat([topic_keyword_year_df,temp_year_df_topic],axis = 1)

        #st.write('Keyword frequency per year and topic')
            #st.write('year',year),
        st.write(f" Showing top keywords for topic id {topic_slider_val}")
        #topic_keyword_year_df
        topic_keyword_year_df = topic_keyword_year_df.fillna(0)
        topic_keyword_year_df = topic_keyword_year_df.astype(int)

        st.dataframe(topic_keyword_year_df.fillna(0))
