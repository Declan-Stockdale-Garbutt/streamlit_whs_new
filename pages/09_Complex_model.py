import streamlit as st
from bertopic import BERTopic
import io
from io import StringIO
#from sentence_transformers import SentenceTransformer
from umap import UMAP
import pandas as pd
import pickle
import base64
import beepy

import time
st.header('Complex model')
st.write(' There is an issue with using the "Upload a previously cleaned file" json file with this method.')
st.write('To mitigate this, reload the cleaned file in the "Upload a json file to clean" section, leave all checkboxes unclicked and click the clean data button')
st.write('The file will be left alone and will be in the correct format for input')


# See if dataframe is uploaded otherwise point to loading page
if 'df_working' not in st.session_state:
    st.write('Please upload a json file in previous page before proceeding with Berttopic modelling')
else:
    df_working = st.session_state['df_working']

    # check that model is already loaded
    if 'complex_model' not in st.session_state:# and 'berttopic_model_df' not in st.session_state:

        if 'complex_model_upload' not in st.session_state:
            st.session_state.complex_model_upload = False

        # init button
        if 'proceed_button_complex' not in st.session_state:
            st.session_state.proceed_button_complex = False

        proceed_button_complex =  st.button('Generate complex model')


        if proceed_button_complex: # button was clicked

            # add button click into memory
            st.session_state.proceed_button_complex = True

            # Create model
            with st.spinner(text="Creating model from documents"):

                # In future add embedding options
                #sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                #embeddings = sentence_model.encode(df_working.Data.values.tolist(), show_progress_bar=True)

                # try to get model to work, sometimes fails with insufficient data, if that occurs, reduce min topic size
                try:
                    berttopic_model = BERTopic(nr_topics = 'auto').fit(df_working.Data.values.tolist())#, embeddings)
                except:
                    st.write('Failed to fit using defaul values, reducing minimum topic size from 10 to 5')
                    berttopic_model = BERTopic(nr_topics = 'auto',min_topic_size = 5).fit(df_working.Data.values.tolist())

            # load model into memory
            st.session_state.complex_model = berttopic_model
            # restart with relevnt thing loaded into memory
            st.experimental_rerun()

        # option to upload model
        st.write("")
        st.subheader('Please upload a previous model')

        uploaded_complex_model = st.file_uploader("",key = 'uploaded_complex_model')

        # Used to determine if option to dopwnload model is shown at end, no point if uploaded model
        if 'was_complex_model_uploaded' not in st.session_state:
            st.session_state.was_complex_model_uploaded = False

        if uploaded_complex_model is not None:
            # unpickle model upload
            berttopic_model = pickle.load(uploaded_complex_model)
            #load into memory
            st.session_state.complex_model = berttopic_model
            st.session_state.was_complex_model_uploaded = True

            # restart with everything needed in memory
            st.experimental_rerun()


    else: # model is uploaded
        st.header("")
        if st.session_state.complex_model is not None:
            st.subheader("Output of model")

            remove_model = st.button('Click to remove model and try again')

            if remove_model:
                # delete session state for model and dataframe
                del st.session_state.complex_model
                st.experimental_rerun()

            if 'berttopic_model_df' not in st.session_state:
                st.session_state.berttopic_model_df = None

                remove_model = st.button('Click to remove model and try again',key = 'remove_model inside loop')

                if remove_model:
                    # delete session state for model and dataframe
                    del st.session_state.complex_model
                    st.experimental_rerun()

                # load model from memory
                berttopic_model = st.session_state.complex_model

                # fit model on documents
                with st.spinner(' Fitting on documents, this may take a while'):
                    bert_topics, bert_probs = berttopic_model.fit_transform(df_working.Data.values.tolist())

                    # Get topic output and score for each document by running docs through model
                    # Join output onto original dataframe
                    topic_series = pd.Series(bert_topics,name = 'bert_topic_id')
                    probability_series = pd.Series(bert_probs, name = 'bert_probability')
                    berttopic_model_df = pd.concat([df_working,topic_series,probability_series],axis = 1)


                    # same the modified dataframe above to memory
                    st.session_state.berttopic_model_df = berttopic_model_df
                    # restart with new df in memory
                    st.experimental_rerun()

            else:
                # everything is loaded into memory to proceed
                berttopic_model_df = st.session_state.berttopic_model_df
                berttopic_model = st.session_state.complex_model

                # get topic info
                topic_information = berttopic_model.get_topic_info()


                st.write("")
                st.subheader('Model output')
                # number of topics
                st.write('number of topics found', len(topic_information))

                # how topic id, document count, Name of topic
                #st.write('topic info',topic_information)

                # create df of 10 highet prob docs for each topic
                df_most_rep_docs = pd.DataFrame()

                for topic in berttopic_model_df['bert_topic_id'].unique():
                    # loop over all topics in df
                    temp_df = berttopic_model_df#
                    # tempdf of all docs fror a single topic
                    temp_df = temp_df[temp_df['bert_topic_id'] == topic]
                    # Sort by bert_probability
                    temp_df = temp_df.sort_values(by='bert_probability', ascending=False)
                    # Just get top 10 values
                    temp_df = temp_df.head(10)
                    # COncat to empty df
                    df_most_rep_docs = pd.concat([df_most_rep_docs,temp_df],axis = 0)

                st.subheader('Top 10 representative documents for each topic')
                st.write(df_most_rep_docs)

                # download functionality
                download_df_most_rep_docs = st.text_input('What would you like to name this file', key = 'download_df_most_rep_docs')
                if download_df_most_rep_docs == "":
                    download_df_most_rep_docs = 'output'


                st.download_button(
                    label="Download output",
                    data=df_most_rep_docs.to_csv(),
                    file_name=download_df_most_rep_docs+'.csv',
                    mime='text/csv'
                )


                # create empty df
                df_most_rep_docs_top_10 = pd.DataFrame()
                for topic in (berttopic_model_df['bert_topic_id'].unique()):
                    # Loop over all topics in df

                    # temp df of all docs for a given topic
                    temp_df = berttopic_model_df[berttopic_model_df['bert_topic_id'] == topic]
                    # Sort by bert_probability
                    temp_df = temp_df.sort_values(by='bert_probability', ascending=False)
                    # Get top 10 valeus
                    temp_df = temp_df.head(10)
                    # Only get title col
                    temp_df = temp_df['Title']
                    # conert to seies
                    temp_df = pd.Series(temp_df,name = ('topic ' + str(topic)))
                    # reset index
                    temp_df = temp_df.reset_index(drop=True)
                    # concat with df
                    df_most_rep_docs_top_10 = pd.concat([df_most_rep_docs_top_10,temp_df],axis = 1)

                # Get current list of columns
                proper_cols = list(set(berttopic_model_df.bert_topic_id.values.tolist()))
                # currently they are int, want to convert to string
                proper_cols = [('topic ' + str(x)) for x in proper_cols]
                # reset based on string col names
                df_most_rep_docs_top_10 = df_most_rep_docs_top_10.reindex(columns=proper_cols)



                st.subheader('Only view by titles')
                st.write(df_most_rep_docs_top_10)

                # download functionality
                download_df_most_rep_docs_top_10 = st.text_input('What would you like to name this file',key = 'download_df_most_rep_docs_top_10')
                if download_df_most_rep_docs_top_10 == "":
                    download_df_most_rep_docs_top_10 = 'output'
                #st.session_state.download_dataframe_with_keywords = download_top_10_for_Each_topic

                st.download_button(
                    label="Download output",
                    data=df_most_rep_docs_top_10.to_csv(),
                    file_name=download_df_most_rep_docs_top_10+'.csv',
                    mime='text/csv'
                )

                # set meory placeholders for each visual, saves them being recalcualted each time
                if 'useful_document_vis' not in st.session_state:
                     st.session_state.useful_document_vis = None

                if 'bert_heatmap' not in st.session_state:
                     st.session_state.bert_heatmap = None

                if 'hierarchical_topics' not in st.session_state:
                     st.session_state.hierarchical_topics = None

                if 'tree_diagram' not in st.session_state:
                     st.session_state.tree_diagram = None

                if 'barchart_top_words' not in st.session_state:
                     st.session_state.barchart_top_words = None

                if 'topics_over_time_fig' not in st.session_state:
                     st.session_state.topics_over_time_fig = None

                     with st.spinner('Loading visuals'):

                        # load  vis and save to memory

                        useful_document_vis = berttopic_model.visualize_documents(berttopic_model_df.Data.values.tolist())
                        st.session_state.useful_document_vis = useful_document_vis

                        bert_heatmap = berttopic_model.visualize_heatmap()
                        st.session_state.bert_heatmap = bert_heatmap

                        hierarchical_topics = berttopic_model.hierarchical_topics(berttopic_model_df.Data.values.tolist())
                        st.session_state.hierarchical_topics = hierarchical_topics

                        tree_diagram = berttopic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
                        st.session_state.tree_diagram = tree_diagram

                        barchart_top_words = berttopic_model.visualize_barchart(top_n_topics=len(topic_information), n_words = 10, height = 400)
                        st.session_state.barchart_top_words = barchart_top_words

                        timestamps = berttopic_model_df.Year.values.tolist()
                        topics_over_time = berttopic_model.topics_over_time(berttopic_model_df.Data.values.tolist(), timestamps)
                        topics_over_time_fig = berttopic_model.visualize_topics_over_time(topics_over_time)
                        st.session_state.topics_over_time_fig = topics_over_time_fig
                        #restart now all visuals are in memory
                        st.experimental_rerun()

                else:
                    st.subheader("Visualisations")
                    st.write("")

                    # need to set these so app doesn't throw an error
                    if 'useful_document_vis' not in st.session_state:
                        st.session_state.useful_document_vis = None

                    if 'bert_heatmap' not in st.session_state:
                        st.session_state.bert_heatmap = None

                    if 'hierarchical_topics' not in st.session_state:
                        st.session_state.hierarchical_topics = None

                    if 'tree_diagram' not in st.session_state:
                        st.session_state.tree_diagram = None

                    if 'barchart_top_words' not in st.session_state:
                        st.session_state.barchart_top_words = None

                    if 'topics_over_time_fig' not in st.session_state:
                        st.session_state.topics_over_time_fig = None

                    #load visuals from memory

                    useful_document_vis = st.session_state.useful_document_vis
                    st.subheader('Visual document embeddings')

                    show_more_useful_document_vis_button = st.button('Click to know more', key = 'show_more_useful_document_vis ')

                    if show_more_useful_document_vis_button:
                        st.write('The figure shows the proximity of topics and the underlying documents. This can be sued to gain insight into what topics are similar to others.')

                        show_more_useful_document_vis_button_close = st.button('Hide', key = 'show_more_useful_document_vis_button_close')

                        if show_more_useful_document_vis_button_close:
                            show_more_useful_document_vis_button ==False

                    st.plotly_chart(useful_document_vis)

                    # download Functionality
                    buffer = io.StringIO()
                    useful_document_vis.write_html(buffer, include_plotlyjs='cdn')
                    html_bytes = buffer.getvalue().encode()

                    st.download_button(
                        label='Download image as HTML',
                        data=html_bytes,
                        file_name='visualised topic clustering.html',
                        mime='text/html'
                    )


                st.write('')
                st.subheader('Heatmap of topics')
                bert_heatmap = st.session_state.bert_heatmap

                show_more_heat_map_button = st.button('Click to know more', key = 'show_more_heat_map_button ')
                if show_more_heat_map_button:
                    st.write('This shows a correlation matrix of how all how much all topics are related. A darker square incdicates more related, wheras a light square indicates less relatedness.')

                    show_more_heat_map_button_close = st.button('Hide', key = 'show_more_heat_map_button_close')

                    if show_more_heat_map_button_close:
                        show_more_heat_map_button ==False

                st.write(bert_heatmap)

                # download Functionality
                st.download_button(
                    label='Download image as HTML',
                    data=html_bytes,
                    file_name='topic heatmap.html',
                    mime='text/html'
                )




                st.write('')
                st.subheader('Hierachial Tree Diagram')
                tree_diagram = st.session_state.tree_diagram

                show_more_tree_diagram_button = st.button('Click to know more', key = 'show_more_tree_diagram_button ')
                if show_more_tree_diagram_button:
                    st.write('This figure indicates how similar topics are. The model finds the most similar topics and joins them into one topic. This is repeated until al topics are joined.')
                    show_more_heat_tree_diagram_close = st.button('Hide', key = 'show_more_tree_diagram_button_close')

                    if show_more_heat_tree_diagram_close:
                        show_more_tree_diagram_button ==False
                st.plotly_chart(tree_diagram)

                # download Functionality
                tree_diagram.write_html(buffer, include_plotlyjs='cdn')
                html_bytes = buffer.getvalue().encode()

                st.download_button(
                    label='Download image as HTML',
                    data=html_bytes,
                    file_name='hierachial topics.html',
                    mime='text/html'
                )

                st.write('')
                st.subheader('Barchart for top 10 words for each topic ')
                barchart_top_words = st.session_state.barchart_top_words
                show_more_barchart_top_words_button = st.button('Click to know more', key = 'show_more_barchart_top_words_button ')
                if show_more_barchart_top_words_button:
                    st.write('This is the top 10 words for each topic found by the complex model')
                    show_more_barchart_top_words_close = st.button('Hide', key = 'show_more_barchart_top_words_button_close')

                    if show_more_barchart_top_words_close:
                        show_more_barchart_top_words_button ==False


                st.plotly_chart(barchart_top_words)

                # download Functionality
                barchart_top_words.write_html(buffer, include_plotlyjs='cdn')
                html_bytes = buffer.getvalue().encode()

                st.download_button(
                    label='Download image as HTML',
                    data=html_bytes,
                    file_name='top words bar chart.html',
                    mime='text/html'
                )

                st.write("")
                st.subheader('Topics over time')
                topics_over_time_fig = st.session_state.topics_over_time_fig

                show_more_topics_over_time_button = st.button('Click to know more', key = 'show_more_topics_over_time_button ')
                if show_more_topics_over_time_button:
                    st.write('This shows how the frequency of each topic changes over time. The timestamps used are the year values within the inital cleaned dataframe.')

                    show_more_topics_over_time_button_close = st.button('Hide', key = 'show_more_topics_over_time_button_close')

                    if show_more_topics_over_time_button_close:
                        show_more_topics_over_time_button ==False

                topics_over_time_fig

                # download Functionality
                topics_over_time_fig.write_html(buffer, include_plotlyjs='cdn')
                html_bytes = buffer.getvalue().encode()

                st.download_button(
                    label='Download image as HTML',
                    data=html_bytes,
                    file_name='Topics over time.html',
                    mime='text/html'
                )
        #######################################
                if st.session_state.was_complex_model_uploaded == True:

                    st.write("")
                    st.subheader(' Option to download the model')
                    download_model_complex = st.text_input('What would you like to name this the model', key = 'download_model_complex')
                    if download_model_complex == "":
                        download_model_complex = 'output'

                    output_model = pickle.dumps(berttopic_model)
                    b64 = base64.b64encode(output_model)#.decode()

                    st.download_button(
                        label="Download model, will be saved as a .pkl file",
                        data=output_model,
                        file_name=download_model_complex+ '.pkl')
