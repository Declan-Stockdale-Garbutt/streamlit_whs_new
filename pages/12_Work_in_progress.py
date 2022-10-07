from __future__ import print_function
import streamlit as st

from streamlit import components

import pyLDAvis
import pyLDAvis.sklearn
#pyLDAvis.enable_notebook()
#from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

st.header('PyLDAVis - not functional yet')
#st.write('Using all-MiniLM-L6-v2 as the embedding model')


if "df_working" not in st.session_state:
    st.write('Please upload a json file in previous page before proceeding with Berttopic modelling')
else:
    df_working = st.session_state['df_working']

    proceed_button_pyldavis =  st.button('Proceed with PyLDAVis')

    if proceed_button_pyldavis:

        tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                    stop_words = 'english',
                    lowercase = True,
                    token_pattern = r'\b[a-zA-Z]{3,}\b',
                    max_df = 0.5,
                    min_df = 10)


        tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
        dtm_tfidf = tfidf_vectorizer.fit_transform(df_working.Data.values.tolist())


        lda_tfidf = LatentDirichletAllocation(n_components=20, random_state=0)
        lda_tfidf.fit(dtm_tfidf)

        st.write(' Visualisation of PyLDAVis')

        pyldavis_vis = pyLDAvis.sklearn.prepare(lda_tfidf, dtm_tfidf, tfidf_vectorizer)
        pyLDAvis.save_html(pyldavis_vis, 'lda.html')
        st.write('pyldavis_vis')
        st.write(pyldavis_vis)
        #pyLDAvis.save_html(pyldavis_vis, 'lda.html')


        #from streamlit import components
        #with open('./lda.html', 'r') as f:
            #html_string = f.read()

        #components.v1.html(html_string, width=1300, height=800, scrolling=False)

        st.write(pyldavis_vis)

        with open('./lda.html', 'r') as f:
            html_string = f.read()
        components.v1.html(html_string, width=1300, height=800, scrolling=False)

        st.write('above as plotly chart')
        st.html(pyldavis_vis)
