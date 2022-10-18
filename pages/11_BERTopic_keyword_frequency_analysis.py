import streamlit as st
from keybert import KeyBERT
from textblob import TextBlob
import pandas as pd
from nltk.corpus import stopwords
stop = stopwords.words('english')
pd.set_option('precision', 0)

st.header('Use keyword extractor to find most common keywords for each year using BERTopic model')
st.write('The Basic keyword analysis and the BERTopic model pages must be run before proceeding.')
st.write('The result of the generated topics for each document and combined with the keyword analysis output')
st.write("An interactive table for each topic is created showing the frequency of keywords over time.")


# is df in memory
if "df_working" not in st.session_state:
    st.subheader('Please upload a json file in previous page before proceeding with BERTopic model')
else:
    # df in memory

    #check that keybert has alrady been performed
    if 'keywords_df' not in st.session_state:
        st.write('Please run Basic keyword analysis to generate keywords then return to this page')
    elif 'bertopic_model_df' not in st.session_state:
        st.subheader('Please run BERTopic model to assign topics for each document then return to this page')
    else:

        # load in df from memory
        df_working = st.session_state.df_working

        # load in modified df from memory
        final_bertopic_df = st.session_state.bertopic_model_df

        # sort dataframes by Title column
        final_bertopic_df = final_bertopic_df.sort_values(by=['Title'])
        # reset index
        final_bertopic_df = final_bertopic_df.reset_index(drop=True)
        # concat dfs
        final_bertopic_df = final_bertopic_df[['bert_topic_id']]#.drop(columns=['Title','bert_probability'],axis =1 )

        # sort by title
        df_working = df_working.sort_values(by=['Title'])
        # reset index
        df_working = df_working.reset_index(drop=True)
        # merge both dfs now they are sorted by title and axis have been dropped
        final_df_t2v = pd.concat([df_working,final_bertopic_df],axis = 1)

        #st.subheader(' BERTopic model keyword analysis')

        st.subheader('Find occurences of keyBert keywords by topic id assigned from BERTopic model over time')

        # initialise slider in memory
        if 'topic_slider_val' not in st.session_state:
            st.session_state.topic_slider_val = False

        # create select slider
        topic_slider_val = st.select_slider('Choose a topic id ', options = sorted(final_df_t2v['bert_topic_id'].unique()),key = 'bert_topic_slider')
        # load value into memory of select slider
        st.session_state.topic_slider_val = topic_slider_val

        # order years 2022,2021,2020 -> 2020, 2021, 2022
        proper_cols_ = list(set(df_working.Year.values.tolist()))
        proper_cols_ = sorted(proper_cols_)

        # init empty df
        topic_keyword_year_df = pd.DataFrame()
        for year in proper_cols_:

            #loop over year and topics
            temp_year_df_topic = final_df_t2v[(final_df_t2v['Year'] == str(year)) & (final_df_t2v['bert_topic_id'] == (topic_slider_val))]

            # Join inidividual words into list
            temp_year_df_topic = pd.Series(' '.join(temp_year_df_topic['keywords_bert']).lower().split(), name = str(year)).value_counts()
            # concat df to previous df
            topic_keyword_year_df = pd.concat([topic_keyword_year_df,temp_year_df_topic],axis = 1)


        st.write(f" Showing top keywords for topic id {topic_slider_val}")

        #topic_keyword_year_df, fill empty with 0
        topic_keyword_year_df = topic_keyword_year_df.fillna(0)
        topic_keyword_year_df = topic_keyword_year_df.astype(int)

        st.dataframe(topic_keyword_year_df.fillna(0))

        # download functionality
        st.download_button(
            label="Download ouptut",
            data=topic_keyword_year_df.fillna(0).to_csv(),
            file_name='bertopic_topic_'+str(topic_slider_val)+'_most_common_words_per_year.csv',
            mime='text/csv'
        )
