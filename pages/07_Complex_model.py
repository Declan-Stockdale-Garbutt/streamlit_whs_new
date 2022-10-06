import streamlit as st
from bertopic import BERTopic
#from sentence_transformers import SentenceTransformer
#from bertopic import BERTopic
from umap import UMAP
import pandas as pd

st.header('Complex model')

# See if datafrsame is uploaded otherwise point to loading page
if "df_working" not in st.session_state:
    st.write('Please upload a json file in previous page before proceeding with Berttopic modelling')
else:
    df_working = st.session_state['df_working']

    # check that model is already loaded
    if 'berttopic_model' not in st.session_state or st.session_state.berttopic_model == False:
        st.session_state.berttopic_model = False
        #st.write('initial st.session_state.berttopic_model', st.session_state.berttopic_model)

        # proceed to create model

        # init button
        if ['proceed_button_bert'] not in st.session_state:
            st.session_state.proceed_button_bert = False

        proceed_button_bert =  st.button('Generate complex model')

        if proceed_button_bert:
            st.session_state.proceed_button_bert = True

            with st.spinner(text="Creating model from documents"):

                #sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                #embeddings = sentence_model.encode(df_working.Data.values.tolist(), show_progress_bar=True)
                st.write('error here?')
                
                st.write('df_working')
                st.write(df_working)
                berttopic_model = BERTopic(nr_topics = 'auto').fit(df_working.Data.values.tolist())#, embeddings)

            with st.spinner(text="Fitting model on documents, this may take a while"):
                bert_topics, bert_probs = berttopic_model.fit_transform(df_working.Data.values.tolist())

            st.session_state.berttopic_model = berttopic_model # new

            if 'bert_topics' not in st.session_state:
                st.session_state.bert_topics = bert_topics

            if 'bert_probs' not in st.session_state:
                st.session_state.bert_probs = bert_probs


            #st.write('after creation st.session_state.berttopic_model', st.session_state.berttopic_model)



    else:
        #st.write(st.session_state.berttopic_model)
        berttopic_model = st.session_state.berttopic_model
        bert_topics = st.session_state.bert_topics
        bert_probs = st.session_state.bert_probs
        #st.write('Model already loaded')
        #st.write('else loop st.session_state.berttopic_model', st.session_state.berttopic_model)

    # Show results here
    #bert_topics = st.session_state.bert_topics
    #bert_probs= st.session_state.bert_probs

    # join topic and probability to original dataframe
    bert_topics = st.session_state.bert_topics
    bert_probs = st.session_state.bert_probs
    topic_series = pd.Series(bert_topics,name = 'bert_topic_id')
    probability_series = pd.Series(bert_probs, name = 'bert_probability')
    berttopic_model_df = pd.concat([df_working,topic_series,probability_series],axis = 1)

    if 'berttopic_model_df' not in st.session_state:
        st.session_state.berttopic_model_df = False



    st.session_state.berttopic_model_df = berttopic_model_df

    # get topic info
    topic_information = berttopic_model.get_topic_info()

    # number of topics
    st.write('number of topics found', len(topic_information))

    # how topic id, document count, Name of topic
    st.write('topic info',topic_information)

    # create df of 10 highet prob docs for each topic
    df_most_rep_docs = pd.DataFrame()
    df_most_rep_docs_v2 = pd.DataFrame()
    for topic in berttopic_model_df['bert_topic_id'].unique():
        #print(topic)

        temp_df = berttopic_model_df#
        temp_df = temp_df[temp_df['bert_topic_id'] == topic]
        temp_df = temp_df.sort_values(by='bert_probability', ascending=False)
        temp_df = temp_df.head(10)
        df_most_rep_docs = pd.concat([df_most_rep_docs,temp_df],axis = 0)

        #temp_df_v2 = df_working
        temp_df_v2 = berttopic_model_df[berttopic_model_df['bert_topic_id'] == topic]
        temp_df_v2 = temp_df_v2.sort_values(by='bert_probability', ascending=False)
        temp_df_v2 = temp_df_v2.head(10)
        temp_df_v2 = temp_df_v2['Title']
        temp_df_v2 = pd.Series(temp_df_v2,name = str(topic))
        temp_df_v2 = temp_df_v2.reset_index(drop=True)
        df_most_rep_docs_v2 = pd.concat([df_most_rep_docs_v2,temp_df_v2],axis = 1)

    # unwieldy df includes all info
    df_most_rep_docs = df_most_rep_docs[df_most_rep_docs['bert_topic_id'] != -1]
    st.write('Top 10 representative documents for each topic',df_most_rep_docs)

    # Get current list of columns
    proper_cols = list(set(berttopic_model_df.bert_topic_id.values.tolist()))
    # currently they are int, want to convert to string
    proper_cols = [str(x) for x in proper_cols]
    # reset based on string col names
    df_most_rep_docs_v2= df_most_rep_docs_v2.reindex(columns=proper_cols)
    #st.write('temp_df_v2',temp_df_v2)
    st.write('Only view by titles')
    st.write(df_most_rep_docs_v2)
    #df_most_rep_docs_v2 = df_most_rep_docs_v2.reindex(sorted(df_most_rep_docs_v2.columns), axis=1)

    # update df_working


    #st.session_state.berttopic_model_df = df_working
    st.subheader("Visualisations")

    if 'useful_document_vis' not in st.session_state:
        st.session_state.useful_document_vis = False

    if st.session_state.useful_document_vis == False:
        with st.spinner('Loading document viewer, reduces embeddings to 2d image'):
            useful_document_vis = berttopic_model.visualize_documents(berttopic_model_df.Data.values.tolist())

        st.session_state.useful_document_vis = useful_document_vis
        st.write(' View document embeddings')
        st.caption('Hover to view')
        st.plotly_chart(useful_document_vis)
    else:
        useful_document_vis = st.session_state.useful_document_vis
        st.write(' View document embeddings')
        st.caption('Hover to view')
        st.plotly_chart(useful_document_vis)

    with st.spinner('Loading heatmap'):
        bert_heatmap = berttopic_model.visualize_heatmap()

    st.write('heatmap')
    st.write(bert_heatmap)


    with st.spinner('Loading inter topic distance mapping'):
        inter_topic_distance = berttopic_model.visualize_topics()

    st.write('Intertopic distance')
    st.plotly_chart(inter_topic_distance)

    with st.spinner('Loading hierarchical tree diagram'):
        hierarchical_topics = berttopic_model.hierarchical_topics(berttopic_model_df.Data.values.tolist())
        tree_diagram = berttopic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)

    st.write('Heirichail tree diagram')
    st.plotly_chart(tree_diagram)


    with st.spinner('Loading barcharts of top 10 words'):
        barchart_top_words = berttopic_model.visualize_barchart(top_n_topics=len(topic_information), n_words = 10, height = 400)

    st.write('barchart')
    st.plotly_chart(barchart_top_words)

    with st.spinner('Loading topics over time'):
        timestamps = berttopic_model_df.Year.values.tolist()

        topics_over_time = berttopic_model.topics_over_time(berttopic_model_df.Data.values.tolist(), timestamps)
        topics_over_time_fig = berttopic_model.visualize_topics_over_time(topics_over_time)

    st.write('Topics over time')
    topics_over_time_fig
