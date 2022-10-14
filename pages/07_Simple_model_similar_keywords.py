import streamlit as st

# is model in memory
if 'top2vec_model' not in st.session_state or st.session_state.top2vec_model == False:


    st.write('Please run Top2Vec model first before looking at this page')

else:
    # model in memory

    # load mdoel from memory
    top2vec_model = st.session_state.top2vec_model

    # load df from memory
    df_working = st.session_state['df_working']

    st.header('Find similar words to a keyword')

    # init output for memory
    if 'keywords_similar' not in st.session_state:
        st.session_state.keywords_similar = False

    st.write("")

    # Text inut
    keywords_similar = st.text_input('')
    # button
    keywords_similar_button =  st.button('Search for keyword')

    if keywords_similar_button: # button was clicked

        # load word from memory
        st.session_state.keywords_similar = keywords_similar
        st.write('Searching for', keywords_similar)

        # look for similar
        try:
            # load keyword into model functionality
            words, word_scores = top2vec_model.similar_words(keywords=[keywords_similar], keywords_neg=[], num_words=20)

            # get output of top 20 words

            # init empty list
            list_of_similar_keywords = []

            # append to dataframe for easier reading
            for word, score in zip(words, word_scores):

                # get word and similaity score
                output = {'Word': word,'Score': score}
                list_of_similar_keywords.append(output)

            st.table(list_of_similar_keywords)

        except:
            # model didn't learn model and error appeared
            st.write(f"Keyword: {keywords_similar} hasn't been learnt by the model, please try another keyword")
