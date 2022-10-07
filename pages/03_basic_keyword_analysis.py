import streamlit as st
from keybert import KeyBERT
from textblob import TextBlob
import pandas as pd
from nltk.corpus import stopwords
#import texthero as hero
stop = stopwords.words('english')
pd.set_option('precision', 0)
#from sklearn.feature_extraction.text import TfidfVectorizer

import subprocess
cmd = ['python3', '-m', 'textblob.download_corpora']
subprocess.run(cmd)
st.write("working")


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

    df_working = st.session_state.df_working

    if 'keywords_df' not in st.session_state:
    # button to perform keyword extraction(s)
        if 'keyword_button_extract' not in st.session_state:
            st.session_state.keyword_button_extract = False

        keyword_button_extract = st.button('Extract nouns and keywords')

        # clicked on button
        if keyword_button_extract:
            st.session_state.proceed_button_t2v = True

            # init text TextBlob
            with st.spinner(' Creating unigrams'):

                df_working['textblob_nouns'] = df_working.apply(lambda row : textblob_nouns(row['Data']), axis=1)
                df_working['textblob_nouns'] = df_working.apply(lambda row : ' '.join(row['textblob_nouns']), axis=1)

            # init keybert
            bert = KeyBERT()
            num_keywords = 20

            with st.spinner('keywords using KeyBert'):

                df_working['keywords_bert'] = bert.extract_keywords(df_working['Data'], keyphrase_ngram_range=(1, 1), stop_words="english", top_n=20)
                df_working['keywords_bert'] = df_working.apply(lambda row : get_gram_after_function(row['keywords_bert']), axis=1)
                df_working['keywords_bert'] = df_working.apply(lambda row : ' '.join(row['keywords_bert']), axis=1)

            st.session_state.keywords_df = df_working

            st.write('Dataframe')
            st.write(df_working)
    else:
        # already performed keywords srun through on orig dataframe



        st.subheader('Inspect dataframe with keywords')

        view_original_dataframe_button = st.button('Click to view df',key='show_orginal_df')

        if view_original_dataframe_button:
            st.table(df_working)

            close_view_df = st.button('close table')
            if close_view_df:
                view_original_dataframe_button = False
        #st.write(df_working)


        output_bert_keywords = pd.Series(' '.join(df_working['keywords_bert']).lower().split(), name = 'occurences').value_counts()[:100]

        st.subheader('Most frequent words across dataframe (Title and Text) using keybert')
        view_dataframe_button = st.button('Click to view df')

        if view_dataframe_button:
            st.table(output_bert_keywords)

            close_view_df = st.button('Close view')
            if close_view_df:
                view_dataframe_button = False



        # keybert year analysis
        keyword_year_df = pd.DataFrame()

        # Get current list of columns
        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        keyword_year_df = pd.DataFrame()
        for year in proper_cols_:

            # skip 2023
            #if year == str(2023):
                #continue
            temp_year_df = df_working[df_working['Year'] == str(year)]
            temp_output = pd.Series(' '.join(temp_year_df['keywords_bert']).lower().split(), name = str(year)).value_counts()[:100]
            keyword_year_df = pd.concat([keyword_year_df,temp_output],axis = 1)

        keyword_year_df = keyword_year_df.fillna(0)
        keyword_year_df = keyword_year_df.astype(int)

        #st.subheader('Keyword occurences per year')
        #st.table(keyword_year_df)

        st.subheader('Keyword occurences per year using keybert')
        view_dataframe_button_year = st.button('Click to view df',key = "view_dataframe_button_year")#)

        if view_dataframe_button_year:
            st.table(keyword_year_df)

            close_view_df_year = st.button('Close view')
            if close_view_df_year:
                view_dataframe_button_year = False


#########
        output_textblob_keywords = pd.Series(' '.join(df_working['textblob_nouns']).lower().split(), name = 'occurences').value_counts()[:100]

        st.subheader('Most frequent words across dataframe (Title and Text) using Textblob')
        view_dataframe_button_textblob = st.button('Click to view df', key = 'view_dataframe_button_textblob')

        if view_dataframe_button_textblob:
            st.table(output_bert_keywords)

            close_view_textblob_df = st.button('Close view')
            if close_view_textblob_df:
                view_dataframe_button = False



        # keybert year analysis
        keyword_textblob_year_df = pd.DataFrame()

        # Get current list of columns
        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        keyword_textblob_year_df = pd.DataFrame()
        for year in proper_cols_:

            temp_year_df = df_working[df_working['Year'] == str(year)]
            temp_output = pd.Series(' '.join(temp_year_df['textblob_nouns']).lower().split(), name = str(year)).value_counts()[:100]
            keyword_textblob_year_df = pd.concat([keyword_textblob_year_df,temp_output],axis = 1)

        keyword_textblob_year_df = keyword_textblob_year_df.fillna(0)
        keyword_textblob_year_df = keyword_textblob_year_df.astype(int)

        st.subheader('Keyword occurences per year using Textblob')
        view_dataframe_button_textblob_year = st.button('Click to view df',key = "view_dataframe_button_textblob_year")#)

        if view_dataframe_button_textblob_year:
            st.table(keyword_textblob_year_df)

            close_view_df_textblob_year = st.button('Close view')
            if close_view_df_textblob_year:
                view_dataframe_button_textblob_year = False
