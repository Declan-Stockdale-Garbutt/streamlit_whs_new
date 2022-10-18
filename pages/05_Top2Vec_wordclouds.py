import streamlit as st
import pandas as pd
from top2vec import Top2Vec
st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Generate Word clouds for Top2Vec model')

# Check that mdoel has been loaded in
if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:


    st.subheader('Please run Top2Vec model first to see results')

else:
    # model exists
    top2vec_model = st.session_state.top2vec_model

    # click to generate ouytput
    st.session_state['show_wordcloud_button'] = True
    top2vec_topic_nums = st.session_state['top2vec_topic_nums']

    # Show how many topics found
    st.write(f"Number of topics found = {top2vec_topic_nums[-1]+1}")
    if "show_wordcloud_button" not in st.session_state:
        st.session_state['show_wordcloud_button'] = False

    st.write('Images can be downloaded by right clicking and saving as png')
    # click to create wordlcouds
    show_wordcloud_button = st.button('Show word cloud for each topic')
    if show_wordcloud_button:

        # loop over topics
        for topic in top2vec_topic_nums:
            # use inbuilt model function to generate wordclouds
            fig = top2vec_model.generate_topic_wordcloud(topic, background_color="black")
            st.pyplot(fig)
