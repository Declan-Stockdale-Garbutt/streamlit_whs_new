import streamlit as st
import json
import pandas as pd
import string
import spacy
sp = spacy.load('en_core_web_sm')
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop = stopwords.words('english')

def text_validity(text):
    words = text.split()
    if len(words) <30 or len(words) > 500:
        return "skip due to length"
    else:
        return text

def title_valid(text):
    words = text.split()
    if len(words) > 30:
        return "skip due to length"
    else:
        return text

def publish_validity(text):
    if len(text) >10:
        return "skip due to length"
    else:

        return text

def publish_weird_format(text, orig):
    if 'unknown' in text or '19:1' in text or '19:S' in text or '198-' in text:

        if ' 20' in text:

            year_info = text
            year_start = year_info.find(' 20')
            year_end = year_start + 9#len(' 2022 Apr')
            year_proper = year_info[year_start:year_end]

            return year_proper

        elif '19' in text:

            year_info = text
            year_start = year_info.find(' 19')
            year_end = year_start + 9
            year_proper = year_info[year_start:year_end]
            #text = year_proper

            return year_proper

        else:
            return orig
            pass
    else:
        return orig

def get_year_from_published(text):
    text = text.strip()
    return text[0:4]

def lemmatise_(text):
    doc_ = sp(text)
    output = " ".join([token.lemma_ for token in doc_ if len(token.lemma_) >2])
    return output



st.markdown(
    """
    # Upload a json file
    #### Please use results from previous page if unsure
    #### Results will be converted to a dataframe

"""
)

#st.write('Upload a json file. Use Document parser option above to prepare json ')
uploaded_json = st.file_uploader("", type = ['json'])#, accept_multiple_files=False)

if uploaded_json is not None:

    json_file = json.load(uploaded_json)


    #st.write(st.session_state[''])

    if "df_working" not in st.session_state:
        st.session_state['df_working'] = ""


    df_working = pd.DataFrame(json_file)
    #st.write(df_working.head())

    original_num_record = df_working.shape[0]

    st.write('### Loading in dataframe')


    current_records = df_working.shape[0]
    df_working['Text'] = df_working.apply(lambda row : text_validity(row['Text']), axis=1)

    current_records = df_working.shape[0]
    df_working['Title'] = df_working.apply(lambda row : title_valid(row['Title']), axis=1)

    current_records = df_working.shape[0]
    df_working['Published'] = df_working.apply(lambda row : publish_validity(row['Published']), axis=1)

    current_records = df_working.shape[0]
    df_working['Published'] = df_working.apply(lambda row : publish_weird_format(row['Journal Information'],row['Published']), axis=1)

    current_records = df_working.shape[0]
    df_working['Year'] = df_working.apply(lambda row : get_year_from_published(row['Published']), axis=1)


    # drop bad data
    # drop rows with unknown in publish date or weird values (only a handful are weird too annoying to fix manually)

    df_working = df_working[df_working['Published'].str.contains('unknown')==False]
    df_working = df_working[df_working['Published'].str.contains('unk')==False]
    df_working = df_working[df_working['Published'].str.contains('1976')==False]

    df_working = df_working[df_working['Title'].str.contains('skip due to length')==False]
    df_working = df_working.reset_index(drop=True)

    st.write('##### Number of records loaded in = ', df_working.shape[0])
    st.write('##### Number of records left out = ',original_num_record - df_working.shape[0])

    df_working["Data"] = df_working["Title"] +" "+ df_working["Text"]




    #######################################################
    st.write('## Perform cleaning on dataframe')

    if 'remove_stopwords_option' not in st.session_state:
        st.session_state.remove_stopwords_option = False

    remove_stopwords_option = st.checkbox('Remove stopwords')

    if 'lemmatise_option' not in st.session_state:
        st.session_state.lemmatise_option = False

    lemmatise_option = st.checkbox('Perform lemmatization')

    if 'remove_punctuation_option' not in st.session_state:
        st.session_state.remove_punctuation_option = False

    remove_punctuation_option = st.checkbox('Remove punctuation')

    if 'clean_data_button' not in st.session_state:
        st.session_state.clean_data_button = False

    clean_data_button = st.button('Clean data')

    if clean_data_button:


        with st.spinner(text="Cleaning dataframe (removing stopwords, punctuation, and performing lemmatitization)... This can take a few minutes"):
        # replace - separtely
            df_working["Data"] = df_working["Data"].replace('-'," ")

            # remove stopwords
            if remove_stopwords_option:
                st.write('removing stopwords')
                df_working["Data"] = df_working["Data"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

            # strip punctuation
            if remove_punctuation_option:
                df_working["Data"] = df_working["Data"].apply(lambda x: ' '.join([word.translate(str.maketrans('', '', string.punctuation)) for word in x.split()]))

            # lemmatise docs
            if clean_data_button:
                df_working['Data'] = df_working.apply(lambda row : lemmatise_(row['Data']), axis=1)

        st.write('#')
        st.write('#### Dataframe to use ' )
        st.write("##### Cleaned data is availaible in the new column 'Data' ")

        st.dataframe(df_working)
        st.session_state['df_working'] = df_working

        st.write('#### Proceed to modelling pages')
