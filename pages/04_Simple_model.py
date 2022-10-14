import streamlit as st
import pandas as pd
from top2vec import Top2Vec
from gensim.models.doc2vec import Doc2Vec
import pickle
import base64

def create_model(dataframe):

    df_working = dataframe

    with st.spinner(text="In progress... This can take a few minutes"):
        try:
            top2vec_model = Top2Vec(df_working['Data'].values.tolist(), embedding_model = 'doc2vec')
        except:
            try:
                st.write('Top2Vec unable to find multiple topics, reducing min topic size')
                top2vec_model = Top2Vec(df_working['Data'].values.tolist(), embedding_model = 'doc2vec',min_count  =2)
            except:
                st.write('trying to chunk docs')
                top2vec_model = Top2Vec(df_working['Data'].values.tolist(), embedding_model = 'doc2vec',min_count  =2,document_chunker = 'sequential',chunk_length = 500, chunk_overlap_ratio = 0.2)

    return top2vec_model



st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Simple Model')

st.write('##### The resulting model is random, refitting the model may result in a different number of topics generated')
#st.write('#### Utilising Top2Vec model to get topics from documents')
st.write("")


if 'df_working' not in st.session_state:
    st.write('Please upload a json file in previous page')
else:
    df_working = st.session_state['df_working']

    if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:
        #st.session_state.top2vec = False

        if 'simple_model_upload' not in st.session_state:
            st.session_state.simple_model_upload = False


        if 'proceed_button_t2v' not in st.session_state:
            st.session_state.proceed_button_t2v = False

        proceed_button_t2v = st.button('Generate simple model')

        if proceed_button_t2v:
            st.session_state.proceed_button_t2v = True

            # Create model
            top2vec_model = create_model(df_working)

            st.session_state.top2vec_model = top2vec_model
            top2vec_topic_sizes, top2vec_topic_nums = top2vec_model.get_topic_sizes()

            st.session_state['top2vec_topic_nums'] = top2vec_topic_nums
            st.experimental_rerun() # why?




        # option to upload model?
        st.write("")
        st.subheader('Upload previously run model here')
        uploaded_simple_model = st.file_uploader("",key = 'uploaded_simple_model')

        if 'simple_model_uploaded' not in st.session_state:
            st.session_state.simple_model_uploaded = False

        if uploaded_simple_model is not None:

            top2vec_model = Top2Vec.load(uploaded_simple_model)
            st.session_state.top2vec_model = top2vec_model
            st.session_state.simple_model_uploaded = True
            st.experimental_rerun()


    #pass
    else:
        st.write("")

        remove_model = st.button('Click to remove model and try again')

        if remove_model:
            del st.session_state['top2vec_model']
            st.experimental_rerun()
            #st.session_state.top2vec_model

        top2vec_model = st.session_state.top2vec_model

        top2vec_topic_sizes, top2vec_topic_nums = top2vec_model.get_topic_sizes()

        st.session_state['top2vec_topic_nums'] = top2vec_topic_nums
        top2vec_topic_nums_series = pd.Series(top2vec_topic_nums,name = 'topic_id')
        top2vec_topic_sizes_series = pd.Series(top2vec_topic_sizes,name = 'topic size')

        st.write('Number of documents in each topic')
        st.table(top2vec_topic_sizes_series)


        final_t2v_df = pd.DataFrame()

        for topic in (top2vec_topic_nums):

            topic_of_interest = topic
            topic_sizes, topic_nums = top2vec_model.get_topic_sizes()
            documents, document_scores, document_ids = top2vec_model.search_documents_by_topic(topic_num=topic_of_interest, num_docs=topic_sizes[topic_of_interest])

            output_top2vec = pd.DataFrame()

            documents_series = pd.Series(documents,name = 'Title')
            document_scores_series = pd.Series(document_scores, name = 't2v_topic_score')
            document_ids_series = pd.Series(document_ids, name = 'document_id')

            output_top2vec = pd.concat([documents_series, document_scores_series,document_ids_series],axis=1)
            output_top2vec['t2v_topic']= topic_of_interest
            #st.write(output_top2vec)
            final_t2v_df = pd.concat([final_t2v_df,output_top2vec])#3

        if 'final_t2v_df' not in st.session_state:
            st.session_state.final_t2v_df = final_t2v_df



        t2v_docs_by_topic = pd.DataFrame()

        for topic in final_t2v_df['t2v_topic'].unique():
            #st.write(topic)
            temp_df = final_t2v_df[final_t2v_df['t2v_topic'] == topic]
            temp_df = temp_df.sort_values(by='t2v_topic_score', ascending=False)
            temp_df = temp_df.head(10)
            t2v_docs_by_topic = pd.concat([t2v_docs_by_topic,temp_df])

        st.subheader('Top 10 documents for each topic')
        t2v_docs_by_topic

        download_top_10_for_Each_topic = st.text_input('What would you like to name this file')
        if download_top_10_for_Each_topic == "":
            download_top_10_for_Each_topic = 'output'
        st.session_state.download_dataframe_with_keywords = download_top_10_for_Each_topic

        st.download_button(
            label="Download dataframe with keywords",
            data=t2v_docs_by_topic.to_csv(),
            file_name=download_top_10_for_Each_topic+'.csv',
            mime='text/csv'
        )

        st.subheader('Top 10 documents for each topic by Title')
        t2v_docs_by_topic_title_only = pd.DataFrame()

        for topic in final_t2v_df['t2v_topic'].unique():

            temp_df = final_t2v_df[final_t2v_df['t2v_topic'] == topic]
            temp_df = temp_df.sort_values(by='t2v_topic_score', ascending=False)
            temp_df = temp_df.head(10)
            temp_df = temp_df['Title']
            temp_df = pd.Series(temp_df,name = ('topic ' + str(topic)))
            temp_df = temp_df.reset_index(drop=True)
            t2v_docs_by_topic_title_only = pd.concat([t2v_docs_by_topic_title_only,temp_df],axis = 1)

        t2v_docs_by_topic_title_only

        download_top_10_by_title = st.text_input('What would you like to name this file', key = 'download_top_10_by_title')
        if download_top_10_by_title == "":
            download_top_10_by_title = 'output'
        st.session_state.download_dataframe_with_keywords = download_top_10_for_Each_topic

        # this was moved
        st.download_button(
            label="Download dataframe with keywords",
            data=t2v_docs_by_topic_title_only.to_csv(),
            file_name=download_top_10_by_title+'.csv',
            mime='text/csv'
        )
        if st.session_state.simple_model_uploaded == False:




            st.write("")
            st.subheader(' Option to download the model')
            download_model_simple = st.text_input('What would you like to name this the model', key = 'download_model_simple')
            if download_model_simple == "":
                download_model_simple = 'output'


            output_model = pickle.dumps(top2vec_model)
            b64 = base64.b64encode(output_model).decode()

            st.download_button(
                label="Download model",
                data=output_model,
                file_name=download_model_simple+ '.pkl'#,
            )
