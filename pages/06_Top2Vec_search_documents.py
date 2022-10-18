import streamlit as st
import pandas as pd
from top2vec import Top2Vec
from transformers import pipeline

# set summariser load to false if not loaded
if 'summariser' not in st.session_state:
    st.session_state['summariser'] = False


def summarise(text): # sshleifer/distilbart-cnn-12-6
    # use defualt huggingface summariser alg, set some parameters
    summary_not_greed = summariser(text, max_length = 120, min_length = 20, do_sample = True)
    output = summary_not_greed[0]['summary_text']

    return output

def Convert(string):
    # split into words
    li = list(string.split(" "))
    return li

def find_docs_using_keyword(keywords, orig_df):
    # set string to " and join as we go"
    output_document = ""

    # default parameters, keyword is input word, num doc = 10
    documents, document_scores, document_ids = top2vec_model.search_documents_by_keywords(keywords=keywords, num_docs=10)# was 10
    # set count to 1 for reading through output
    count = 1

    # get outputs from model doc = document, score = how similar, cod_id is indix location in loaded file
    for doc, score, doc_id in zip(documents, document_scores, document_ids):
        st.write(f"Result number: {count}")
        output_document = output_document + (f"Result number: {count}")
        output_document = output_document + "\n\n"

        st.write(f"Document id in dataframe: {doc_id}, Score: {score}")
        output_document = output_document + str((f"Document id in dataframe: {doc_id}, Score: {score}"))
        output_document = output_document + "\n\n"

        st.write('Title')
        output_document = output_document + 'Title'
        output_document = output_document + "\n\n"


        st.write(orig_df['Title'][doc_id])
        output_document = output_document + str(orig_df['Title'][doc_id])
        output_document = output_document + "\n\n"

        st.write('Text body')
        output_document = output_document + 'Text body'
        output_document = output_document + "\n\n"

        st.write(orig_df['Text'][doc_id])
        output_document = output_document + str((orig_df['Text'][doc_id]))
        output_document = output_document + "\n\n"

        st.write('Summary')
        output_document = output_document + 'Summary'
        output_document = output_document + "\n\n\n"


        count +=1

        # skip if length is poor, failed to sumamrise
        if 'skip due to length' in orig_df['Text'][doc_id].lower():
            st.write('Failed to summarize')
            #output_document.append('Failed to summarize')

            output_document = output_document + 'Failed to summarize'
            output_document = output_document + "\n\n"

        # else summarise
        else:

            try:
                summary_of_document = summarise(orig_df['Text'][doc_id])
                st.write(summary_of_document)
            except:
                summary_of_document = 'Failed to summarise'


            output_document = output_document + str(summary_of_document)
            output_document = output_document + "\n\n"

        st.write("-----------")
        output_document = output_document +str("----------- \n\n")

        st.write()
        #output_string = output_document.append("\n\n")

    return output_document#output_document

st.header('Input keyword and get out first 10 documents most similar to keyword')
st.write("The displayed output is the title, the text, and a  ~ 100 word summarisation which can be downloaded")
st.write(' The summarisation is performed using a summarisation model from HuggingFace')

if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:


    st.subheader('Please run Top2Vec model first to see results')

else:
    # model has been created

    # laod model from memory
    top2vec_model = st.session_state.top2vec_model
    # load dataframe from memory
    df_working = st.session_state['df_working']



    # add keyword to memory
    if 'keywords_' not in st.session_state:
        st.session_state.keywords_ = False

    # keyword input
    keywords_ = st.text_input('Find documents with keywords')#.to_list()
    # button press
    proceed_button_t2v =  st.button('Search for documents similar to keyword')

    if proceed_button_t2v:
        # button was clicked

        if st.session_state['summariser'] == False:

            # wait for model to load
            with st.spinner('Loading summarisation model'):
                summariser = pipeline('summarization')

            # load summariser into memory
            st.session_state.summariser = summariser
            st.write('Summarisation model loaded successfully')

        else:
            # summariser already loaded

            # load summariser from memory
            summariser = st.session_state.summariser

        #del st.session_state.summarised_documents

        st.session_state.keywords_ = keywords_

        # start summarising
        if 'summarised_documents' not in st.session_state:

            with st.spinner(text="In progress... This can take a few minutes"):
                summarised_documents = find_docs_using_keyword(Convert(keywords_),df_working)

            st.write('Done')

            # load ouput into memory
            st.session_state.summarised_documents = summarised_documents

            if "save_sumamarised_documents_button" not in st.session_state:
                st.session_state.save_sumamarised_documents_button = False

            st.write("")
            st.subheader(' Option to download the output')

            # download functionality
            save_sumamarised_documents_button = st.download_button(
                                                    label = 'Download output',
                                                    data = str(summarised_documents),
                                                    file_name=keywords_+ '.txt')
