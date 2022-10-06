import streamlit as st
import pandas as pd
from top2vec import Top2Vec
st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Generate Word clouds for Top2Vec model')

if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:
    #st.session_state.top2vec_model = False

    st.write('Please run Top2Vec model first before looking at this page')

else:
    top2vec_model = st.session_state.top2vec_model

    st.session_state['show_wordcloud_button'] = True
    top2vec_topic_nums = st.session_state['top2vec_topic_nums']

    st.write(f"Number of topics found = {top2vec_topic_nums[-1]+1}")
    if "show_wordcloud_button" not in st.session_state:
        st.session_state['show_wordcloud_button'] = False

    show_wordcloud_button = st.button('Show word cloud for each topic')
    if show_wordcloud_button:
        #st.session_state['show_wordcloud_button'] = True
        #top2vec_topic_nums = st.session_state['top2vec_topic_nums']
        for topic in top2vec_topic_nums:

            fig = top2vec_model.generate_topic_wordcloud(topic, background_color="black")
            st.pyplot(fig)

            #st.write('As list')
            #top2vec_model.topic_words(topic)
