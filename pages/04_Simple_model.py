import streamlit as st
import pandas as pd
from top2vec import Top2Vec
from gensim.models.doc2vec import Doc2Vec
st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Simple Model')

st.write('##### The resulting model may be  The process is random, refitting the model may result in a different number of topics generated')
#st.write('#### Utilising Top2Vec model to get topics from documents')
st.write("")


#st.write('testing df_working sessison state')
if "df_working" not in st.session_state:
    st.write('Please upload a json file in previous page')
else:
    df_working = st.session_state['df_working']
#################################
##################################
    if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:
        #st.session_state.top2vec = False


        if ['proceed_button_t2v'] not in st.session_state:
            st.session_state.proceed_button_t2v = False

        proceed_button_t2v = st.button('Generate simple model')

        if proceed_button_t2v:
            st.session_state.proceed_button_t2v = True

            with st.spinner(text="In progress... This can take a few minutes"):
                top2vec_model = Top2Vec(df_working['Data'].values.tolist(), embedding_model = 'doc2vec')

            st.session_state.top2vec_model = top2vec_model
            top2vec_topic_sizes, top2vec_topic_nums = top2vec_model.get_topic_sizes()

            st.session_state['top2vec_topic_nums'] = top2vec_topic_nums
            top2vec_topic_nums_series = pd.Series(top2vec_topic_nums,name = 'topic_id')
            top2vec_topic_sizes_series = pd.Series(top2vec_topic_sizes,name = 'topic size')

            st.write('Number of documents in each topic')
            st.write(top2vec_topic_sizes_series)

        top2vec_topic_sizes, top2vec_topic_nums = top2vec_model.get_topic_sizes()

        st.session_state['top2vec_topic_nums'] = top2vec_topic_nums
        top2vec_topic_nums_series = pd.Series(top2vec_topic_nums,name = 'topic_id')
        top2vec_topic_sizes_series = pd.Series(top2vec_topic_sizes,name = 'topic size')

        st.write('Number of documents in each topic')
        st.table(top2vec_topic_sizes_series)

        final_t2v_df = pd.DataFrame()

        for topic in (top2vec_topic_nums):
            #st.write(topic)
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
            final_t2v_df = pd.concat([final_t2v_df,output_top2vec])
        final_t2v_df

        if 'final_t2v_df' not in st.session_state:
            st.session_state.final_t2v_df = final_t2v_df

    else:
        st.write("")
        st.write('### Model already created')

        top2vec_model = st.session_state.top2vec_model

        top2vec_topic_sizes, top2vec_topic_nums = top2vec_model.get_topic_sizes()

        st.session_state['top2vec_topic_nums'] = top2vec_topic_nums
        top2vec_topic_nums_series = pd.Series(top2vec_topic_nums,name = 'topic_id')
        top2vec_topic_sizes_series = pd.Series(top2vec_topic_sizes,name = 'topic size')

        st.write('Number of documents in each topic')
        st.table(top2vec_topic_sizes_series)


        final_t2v_df = pd.DataFrame()

        for topic in (top2vec_topic_nums):
            #st.write(topic)
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
