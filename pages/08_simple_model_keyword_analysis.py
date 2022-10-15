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
    # get proper formatting
    words, _ = map(list, zip(*list_))
    return words

st.header('Use Basic keyword analysis to find most common keywords for each year')

st.write('Run Basisc keyword analysis and Simple model before loading this page.')
st.write('The simple model generates topic for each document while the keyword extactor generates keywords')
st.write('Both of these output are necessary to show relevant keywords for each topic.')
# does df exists in memory
if "df_working" not in st.session_state:
    st.subheader('Please upload a json file before proceeding')
else:
    # df does exist in memory

    #check that keybert has alrady been performed
    if 'keywords_df' not in st.session_state:
        st.write('Please run Basic keyword analysis to generate keywords then return to this page')
    elif 'final_t2v_df' not in st.session_state:
        st.write('Please run simple model to assign topics for each document then return to this page')
    else:

        # everything has been done so can proceed

        # load df from memory
        df_working = st.session_state.df_working
        # load keyword df from memory
        final_t2v_df = st.session_state.final_t2v_df

        #below is done to merge keywords . Need to sort and remove  a column, to merge

        # sort dataframes by Title column
        final_t2v_df = final_t2v_df.sort_values(by=['Title'])
        final_t2v_df = final_t2v_df.reset_index( drop=True)
        final_t2v_df = final_t2v_df.drop(columns=['Title','document_id'],axis =1 )

        # sort by title and reset index
        df_working = df_working.sort_values(by=['Title'])
        df_working = df_working.reset_index(drop=True)

        # merge keywords, simple model topics for ocs and original df.
        # needed to sort by Title and then drop TItle otheriwise duplicate column error occurs
        # By sorting, they remain in the same orer
        final_df_t2v = pd.concat([df_working,final_t2v_df],axis = 1)

        # ready to model
        st.subheader(' Simple model keyword analysis')
        view_simple_model_button = st.button('View keywords on simple model',key = "view_simple_model_button")


        # click to view
        if view_simple_model_button:
            st.dataframe(final_df_t2v)

            # click to close
            close_view_df_year = st.button('Close view')
            if close_view_df_year:
                view_simple_model_button = False


        # adding slider
        st.subheader('Find occurences of Bert keywords by topic id over time')
        if 'topic_slider_val' not in st.session_state:
            st.session_state.topic_slider_val = False

        # create select slider
        topic_slider_val = st.select_slider('Choose a topic id ', options = sorted(final_df_t2v['t2v_topic'].unique()),key = 'bert_topic_slider')
        # load currentlsider value into memory
        st.session_state.topic_slider_val = topic_slider_val

        # get list of columns i want ,before this tey topics are unordered 2,1,3, want to order them 1,2,3 etc
        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        # initialise empty df
        topic_keyword_year_df = pd.DataFrame()

        # loop over years in df
        for year in proper_cols_:

            # get year and words for each topic
            temp_year_df_topic = final_df_t2v[(final_df_t2v['Year'] == (year)) & (final_df_t2v['t2v_topic'] == (topic_slider_val))]

            # Append to dataframe above
            temp_year_df_topic = pd.Series(' '.join(temp_year_df_topic['keywords_bert']).lower().split(), name = (year)).value_counts()
            topic_keyword_year_df = pd.concat([topic_keyword_year_df,temp_year_df_topic],axis = 1)

        st.write(f" Showing top keywords for topic id {topic_slider_val}")

        # Fill empty with 0 as some words don't occur in some years or for some topics
        topic_keyword_year_df = topic_keyword_year_df.fillna(0)
        topic_keyword_year_df = topic_keyword_year_df.astype(int)

        # show output
        st.dataframe(topic_keyword_year_df.fillna(0))

        # download functionality
        st.download_button(
            label="Download ouptut",
            data=topic_keyword_year_df.fillna(0).to_csv(),
            file_name='Simple_topic_'+str(topic_slider_val)+'_most_common_words_per_year.csv',
            mime='text/csv'
        )
