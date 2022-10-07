import streamlit as st
from keybert import KeyBERT
from textblob import TextBlob
import pandas as pd
from nltk.corpus import stopwords
#import texthero as hero
stop = stopwords.words('english')
pd.set_option('precision', 0)
#from sklearn.feature_extraction.text import TfidfVectorizer

@st.cache()
def keybert_extractor(text, min=1, max=5):
    """
    Uses KeyBERT to extract the top n keywords from a text
    Arguments: text (str)
    Returns: list of keywords (list)
    """
    keywords = bert.extract_keywords(text, keyphrase_ngram_range=(min, max), stop_words="english", top_n=num_keywords)
    results = []
    for scored_keywords in keywords:
        for keyword in scored_keywords:
            if isinstance(keyword, str):
                results.append(keyword)
    return results

def textblob_nouns(text):
    blob = TextBlob(text)

    return blob.noun_phrases#, blob.ngrams(n=1), blob.ngrams(n=2), blob.ngrams(n=3)


def textblob_ngrams(text,ngram=1):
    blob = TextBlob(text)
    result = blob.ngrams(n=ngram)
    result_str = " ".join([gram[0] for gram in result if gram[0] not in (stop)])

    return result_str

bert = KeyBERT()
def keybert_extractor(text, min=1, max=5,num_keywords = 20):
    """
    Uses KeyBERT to extract the top n keywords from a text
    Arguments: text (str)
    Returns: list of keywords (list)
    """
    keywords = bert.extract_keywords(text, keyphrase_ngram_range=(min, max), stop_words="english", top_n=num_keywords)
    results = []
    for scored_keywords in keywords:
        for keyword in scored_keywords:
            if isinstance(keyword, str):
                results.append(keyword)
    return results

def get_gram_after_function(list_):

    words, _ = map(list, zip(*list_))
    #words
    return words

st.header('Use keyword extractor to find most common keywords for each year')

if "df_working" not in st.session_state:
    st.write('Please upload a json file in previous page before proceeding with Berttopic modelling')
else:
    #check that keybert has alrady been performed
    if 'keywords_df' not in st.session_state:
        st.write('Please run Basic keyword analysis to generate keywords then return to this page')
    elif 'final_t2v_df' not in st.session_state:
        st.write('Please run simple model to assign topics for each document then return to this page')
    else:
        df_working = st.session_state.df_working
        final_t2v_df = st.session_state.final_t2v_df

        # sort dataframes by Title column
        final_t2v_df = final_t2v_df.sort_values(by=['Title'])
        final_t2v_df = final_t2v_df.reset_index( drop=True)
        final_t2v_df = final_t2v_df.drop(columns=['Title','document_id'],axis =1 )


        df_working = df_working.sort_values(by=['Title'])
        df_working = df_working.reset_index(drop=True)

        final_df_t2v = pd.concat([df_working,final_t2v_df],axis = 1)

        # ready to model

        st.subheader(' Simple model keyword analysis')
        view_simple_model_button = st.button('View keywords on simple model',key = "view_simple_model_button")

        #if 'view_simple_model_button' not in st.session_state:

        if view_simple_model_button:
            st.dataframe(final_df_t2v)

            close_view_df_year = st.button('Close view')
            if close_view_df_year:
                view_simple_model_button = False




        st.subheader('Find occurences of Texblob keywords by topic id over time')
        if 'topic_slider_val' not in st.session_state:
            st.session_state.topic_slider_val = False

        topic_slider_val = st.select_slider('Choose a topic id ', options = sorted(final_df_t2v['t2v_topic'].unique()))
        st.session_state.topic_slider_val = topic_slider_val


        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        topic_keyword_year_df = pd.DataFrame()
        for year in proper_cols_:
            temp_year_df_topic = final_df_t2v[(final_df_t2v['Year'] == (year)) & (final_df_t2v['t2v_topic'] == (topic_slider_val))]
            #st.write('temp_year_df_topic', temp_year_df_topic)

            temp_year_df_topic = pd.Series(' '.join(temp_year_df_topic['textblob_nouns']).lower().split(), name = (year)).value_counts()
            topic_keyword_year_df = pd.concat([topic_keyword_year_df,temp_year_df_topic],axis = 1)

        #st.write('Keyword frequency per year and topic')
            #st.write('year',year),
        st.write(f" Showing top keywords for topic id {topic_slider_val}")
        #topic_keyword_year_df
        topic_keyword_year_df = topic_keyword_year_df.fillna(0)
        topic_keyword_year_df = topic_keyword_year_df.astype(int)

        st.dataframe(topic_keyword_year_df.fillna(0))

###################
# adding Textblob
        st.subheader('Find occurences of Bert keywords by topic id over time')
        if 'topic_slider_val' not in st.session_state:
            st.session_state.topic_slider_val = False

        topic_slider_val = st.select_slider('Choose a topic id ', options = sorted(final_df_t2v['t2v_topic'].unique()),key = 'bert_topic_slider')
        st.session_state.topic_slider_val = topic_slider_val


        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        topic_keyword_year_df = pd.DataFrame()
        for year in proper_cols_:
            temp_year_df_topic = final_df_t2v[(final_df_t2v['Year'] == (year)) & (final_df_t2v['t2v_topic'] == (topic_slider_val))]
            #st.write('temp_year_df_topic', temp_year_df_topic)

            temp_year_df_topic = pd.Series(' '.join(temp_year_df_topic['keywords_bert']).lower().split(), name = (year)).value_counts()
            topic_keyword_year_df = pd.concat([topic_keyword_year_df,temp_year_df_topic],axis = 1)

        #st.write('Keyword frequency per year and topic')
            #st.write('year',year),
        st.write(f" Showing top keywords for topic id {topic_slider_val}")
        #topic_keyword_year_df
        topic_keyword_year_df = topic_keyword_year_df.fillna(0)
        topic_keyword_year_df = topic_keyword_year_df.astype(int)

        st.dataframe(topic_keyword_year_df.fillna(0))
