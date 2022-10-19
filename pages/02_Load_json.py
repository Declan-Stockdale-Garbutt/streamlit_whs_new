import streamlit as st
import json
import pandas as pd
import string
import re
import spacy
sp = spacy.load('en_core_web_sm')
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop = stopwords.words('english')

def remove_stopwords(text):
    text = ' '.join([word for word in text.split() if word not in (stop)])
    return text

def remove_punctuation(text):
    text = ' '.join([word.translate(str.maketrans('', '', string.punctuation)) for word in text.split()])
    return text

def lemmatise_(text):
    # lemmatise words using spacy functionality
    doc_ = sp(text)
    output = " ".join([token.lemma_ for token in doc_ if len(token.lemma_) >2])
    return output

def remove_chunk_from_data(text):
    if '_chunk_' in text:
        # find start of chunk
        chunk_start = text.find('_chunk_')
        temp = text[chunk_start:]
        space_after_chunk = temp.find(" ")

        result = text[:chunk_start]+text[chunk_start+space_after_chunk:]
        return result
    else:
        return text

def remove_numbers_from_text(text):
    # remove numbers from text using regex
    pattern = r'[0-9]'
    no_numbers = re.sub(pattern, '', text)
    return no_numbers

def replace_dash_with_space(text):
    text = text.replace('-'," ")
    return text

st.markdown(
    """
    # Upload a json file
    #### Please use results from previous page if unsure
    #### Results will be converted to a dataframe and displayed

"""
)

# upload file
uploaded_json = st.file_uploader("", type = ['json'])

# wait until file has been uploaded
if uploaded_json is not None:

    # load file to json
    json_file = json.load(uploaded_json)

    # Make sure session state exists if not create it
    if 'df_working' not in st.session_state:
        st.session_state.df_working = ""

    # put json in df
    df_working = pd.DataFrame(json_file)

    # how many records in uploaded df
    original_num_record = df_working.shape[0]

    st.write('### Loading in dataframe')

    # drop bad data
    # drop rows with unknown in publish date or weird values (only a handful are weird too annoying to fix manually)
    df_working = df_working[df_working['Published Date'].str.contains('unknown')==False]
    df_working = df_working[df_working['Published Date'].str.contains('unk')==False]
    df_working = df_working[df_working['Published Date'].str.contains('1976')==False]

    df_working = df_working[df_working['Year'].str.contains('unknown')==False]

    df_working = df_working[df_working['Title'].str.contains('skip due to length')==False] # this didn't work
    df_working = df_working[df_working['Text'].str.contains('skip due to length')==False] # this didn't work
    df_working = df_working.reset_index(drop=True)

    st.write('##### Number of records loaded in = ', df_working.shape[0])
    st.write('##### Number of records left out = ',original_num_record - df_working.shape[0])

    df_working["Data"] = df_working["Title"] +" "+ df_working["Text"]
    df_working['Data'] = df_working.apply(lambda row : remove_chunk_from_data(row['Data']), axis=1)
    df_working['Data'] = df_working.apply(lambda row : remove_numbers_from_text(row['Data']), axis=1)
    df_working['Data'] = df_working.apply(lambda row : replace_dash_with_space(row['Data']), axis=1)





    #######################################################
    st.subheader('Perform cleaning on dataframe')
    st.write('Note: BERTopic has been trained on texts that contains stopwords and punctuation. Removing stopwords may impact the models performance.')
    st.write(' Stop words will be more prevalent if with a lower number of documents. It may be worth removing them even if using the BERTopic model.')
    # Check box option
    if 'remove_stopwords_option' not in st.session_state:
        st.session_state.remove_stopwords_option = False

    remove_stopwords_option = st.checkbox('Remove stopwords')

    # Check box option
    if 'lemmatise_option' not in st.session_state:
        st.session_state.lemmatise_option = False

    lemmatise_option = st.checkbox('Perform lemmatization')

    # Check box option
    if 'remove_punctuation_option' not in st.session_state:
        st.session_state.remove_punctuation_option = False

    remove_punctuation_option = st.checkbox('Remove punctuation')

    if 'clean_data_button' not in st.session_state:
        st.session_state.clean_data_button = False

    clean_data_button = st.button('Clean data')

    if clean_data_button:
        st.session_state.clean_data_button = True

    if st.session_state.clean_data_button == True:

        with st.spinner(text="Cleaning dataframe using selected criteria ... This can take a few minutes"):

            # remove stopwords
            if remove_stopwords_option and clean_data_button:
                #df_working["Data"] = df_working["Data"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
                df_working["Data"] = df_working.apply(lambda row: remove_stopwords(row['Data']), axis=1)

            # strip punctuation
            if remove_punctuation_option and clean_data_button: #remove_punctuation
                #df_working["Data"] = df_working["Data"].apply(lambda x: ' '.join([word.translate(str.maketrans('', '', string.punctuation)) for word in x.split()]))
                df_working['Data'] = df_working.apply(lambda row : remove_punctuation(row['Data']), axis=1)

            # lemmatise docs
            if lemmatise_option and clean_data_button:
                df_working['Data'] = df_working.apply(lambda row : lemmatise_(row['Data']), axis=1)

        st.write('#')
        st.write('#### Dataframe to use ' )
        st.write("##### Cleaned data is availaible in the new column 'Data' ")

        st.dataframe(df_working)

        # set session state for later loading
        st.session_state.df_working = df_working

        # save functionality
        write_filename_text = st.text_input('Enter name for file to download file and press Enter')
        if write_filename_text == "":
            write_filename_text = 'output'
        ### option to download the cleaned def
        st.download_button(
            label="Download cleaned output as json",
            data=st.session_state['df_working'].to_json(),
            file_name=write_filename_text+'.json',
            mime='text/json'
        )

        st.write('#### Proceed to modelling pages')

else:
    # Opion to load inn prviosuly cleaned file

    st.write("")
    st.write("")
    st.write("")
    st.subheader('Upload a previously cleaned file')
    uploaded_cleaned_dataframe = st.file_uploader("")

    if uploaded_cleaned_dataframe is not None:

        # Convert file to json
        uploaded_cleaned_dataframe = json.load(uploaded_cleaned_dataframe)
        # Load is as df
        uploaded_cleaned_dataframe = pd.DataFrame.from_dict(uploaded_cleaned_dataframe)

        st.write("")
        st.subheader('Uploaded file as a dataframe')
        uploaded_cleaned_dataframe
        st.write('#### Proceed to modelling pages')

        # store uploaded dataframe into app memory
        st.session_state.df_working = uploaded_cleaned_dataframe
