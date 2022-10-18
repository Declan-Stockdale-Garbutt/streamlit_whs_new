import streamlit as st
from keybert import KeyBERT
from textblob import TextBlob
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop = stopwords.words('english')
pd.set_option('precision', 0)

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

def get_gram_after_function(list_):
    # Get n gram
    words, _ = map(list, zip(*list_))
    #words
    return words

st.subheader('Use keyword extractor to find most common keywords for each year using KeyBERT')
st.write('Running this page is optional but offers additional insight about word frequencies')
st.write("KeyBERT is an advanced keyword extraction package that utilizes a language model")
st.write("")
st.write('Warning will disappear once button is clicked')
st.write("")
st.write("")

# Chekc dataframe exists
if "df_working" not in st.session_state:
    st.subheader('Please upload a json file in previous page before proceeding with Berttopic modelling')

else:
    # Load in dataframe
    df_working = st.session_state.df_working

    # Chekc if keywords analysis ahs been done
    if 'keywords_df' not in st.session_state:

    # button to perform keyword extraction
        if 'keyword_button_extract' not in st.session_state:
            st.session_state.keyword_button_extract = False

        keyword_button_extract = st.button('Extract keywords')

        # clicked on button
        if keyword_button_extract:
            st.session_state.proceed_button_t2v = True # why is this called this?

            # init keybert
            bert = KeyBERT()

            with st.spinner('Extracting keywords using KeyBert... This may take a while'):

                df_working['keywords_bert'] = bert.extract_keywords(df_working['Data'], keyphrase_ngram_range=(1, 1), stop_words="english", top_n=25)
                df_working['keywords_bert'] = df_working.apply(lambda row : get_gram_after_function(row['keywords_bert']), axis=1)
                df_working['keywords_bert'] = df_working.apply(lambda row : ' '.join(row['keywords_bert']), axis=1)

            st.session_state.keywords_df = df_working

    if st.session_state.keywords_df is not None:
        df_working = st.session_state.keywords_df

        st.subheader('Inspect dataframe with keywords')

        st.dataframe(df_working)

        # Save functionality
        download_dataframe_with_keywords = st.text_input('What would you like to name this file')
        if download_dataframe_with_keywords == "":
            download_dataframe_with_keywords = 'output'
        st.session_state.download_dataframe_with_keywords = download_dataframe_with_keywords

        st.download_button(
            label="Download dataframe with keywords",
            data=df_working.to_csv(),
            file_name=download_dataframe_with_keywords+'.csv',
            mime='text/csv'
        )



        output_bert_keywords = pd.Series(' '.join(df_working['keywords_bert']).lower().split(), name = 'occurences').value_counts()[:100]

        st.subheader('Most frequent words across dataframe (Title and Text) using keybert')
        st.dataframe(output_bert_keywords)


        most_frequent_words_df_name = st.text_input('What would you like to name this file', key = 'most_frequent_words_df_name')
        if most_frequent_words_df_name == "":
            most_frequent_words_df_name = 'output'

        # Save functionality
        st.download_button(
            label="Download keyword table",
            data=output_bert_keywords.to_csv(),
            file_name=most_frequent_words_df_name+'.csv',
            mime='text/csv'
        )


        # keybert year analysis
        keyword_year_df = pd.DataFrame()

        # Get current list of columns
        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        # create new dataframe to find keywords by year
        keyword_year_df = pd.DataFrame()
        for year in proper_cols_:
            temp_year_df = df_working[df_working['Year'] == str(year)]
            temp_output = pd.Series(' '.join(temp_year_df['keywords_bert']).lower().split(), name = str(year)).value_counts()[:100]
            keyword_year_df = pd.concat([keyword_year_df,temp_output],axis = 1)

        keyword_year_df = keyword_year_df.fillna(0)
        keyword_year_df = keyword_year_df.astype(int)


        st.subheader('Keyword occurences per year using keybert')
        st.dataframe(keyword_year_df)

        # Save Functionality
        download_keyword_dataframe_text = st.text_input('What would you like to name this file', key = 'download_keyword_dataframe_text')
        if download_keyword_dataframe_text == "":
            download_keyword_dataframe_text = 'output'

        st.download_button(
            label="Download keyword table",
            data=keyword_year_df.to_csv(),
            file_name=download_keyword_dataframe_text+'.csv',
            mime='text/csv'
        )
