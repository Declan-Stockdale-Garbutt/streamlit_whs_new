import streamlit as st
import pandas as pd
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import collections
from collections import Counter

def get_year_from_publishedAt(text):
    # Get first 4 digits of published data to extract year
    text = text[0:4]
    return text

def get_data_from_elastic(index_name):

    # Scan function to get all the data.
    rel = scan(client=es,
               #query=query,
               scroll='1m',
               index=index_name,
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)

    # Keep response in a list.
    result = list(rel)

    temp = []

    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    for hit in result:
        temp.append(hit['_source'])

    # Create a dataframe.
    df = pd.DataFrame(temp)

    return df

def remove_links(text):
    # remove hypertext
    text = str(text)
    if '<a href' in text:
        text = text[:text.find('<a href')]
        return text
    else:
        return text

def find_200_char_limit(text):
    # text over 200 chars end in [+100 chars not shown]
    # Find that extra bit and remove it

    if '[+' in text:
        text = text[:text.find('[+')]
        return text
    else:
        return text

def find_unique_words(text):
    # Find  num of unique words i  a text
    num_unique_words = len(set(text.split()))
    return (num_unique_words)

def find_column_with_more_unique_words(text1, text2):
    # Sometimes main text has title repeated, while another col has proper text.
    # Use this to find which one hsa most unique words (less stuff repeated
    # Return the one with the most unique words as main text
    if find_unique_words(text1) >= find_unique_words(text2):
        return text1
    else:
        return text2

def fix_publisher_eric(text):
    text = text[text.find('\\\n0      ')+len('\\\n0      '):]
    text = text[:text.find('...')]
    return text

def fix_missing_published_by(text):
    if len(text)<3:
        text = 'unknown'

    return text

def remove_whitespace(text):
    text = text.strip() # not working as intended
    text = text.rstrip()
    return text

# Get data from ElastiSearch
es = Elasticsearch(
    cloud_id="WHS:YXVzdHJhbGlhLXNvdXRoZWFzdDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGNhYTExYzViNzQ3YjQwMzViZWFhNzQ1MTcwY2EwOWZlJDZkOWQxNzg1ZjM1MDQxMDdhOTcxMWYyMWU5YjE3ZmQx",
    basic_auth=("elastic", "BnV9bouQp2Pbksh0Zla8Ow78")
)
st.header(' Pull data from Elasic Search database')
st.write("")
st.write('The current implementation pulss all data cuurrently within either the news or the ERIC database')
st.write("Additional funcitonality to search will be included soon")

st.write("")
st.subheader('Pull news from Elastic Search')
st.write("")
st.write(' The newsapi package is used to scrape various news articles from a variety of major news outlets on the web which are uploaded into Elastic Search.')
st.write(' The Free model used for this prototype is limited to the first ~200 characters.')
st.write(' As this is a proof of concept, we only aim to prove the potential usage of this functionality.')
st.write("")

news_elastic_button = st.button('Click to pull news from Elastic Search', key = 'news_elastc_button')

if 'news_elastic_button' not in st.session_state:
    st.session_state.news_elastic_button = False

if "news_df_created" not in st.session_state:
    st.session_state.news_df_created = False

if "news_df" not in st.session_state:
    st.session_state.news_df = False

if news_elastic_button or st.session_state.news_elastic_button:
    st.session_state.news_elastic_button = True
    # Put into database

    if st.session_state.news_df_created == False:
        with st.spinner('Pulling news from Elastic search'):
            df_news = get_data_from_elastic("search-index-whs-news")

        # get necessary columns
        df_news_working = df_news[['title', 'description', 'content', 'url', 'source_name','publishedAt']]
        df_news_working['Language'] = 'en'

        # Define institution using source e.g. news oputlet, necessary for combiing with academic output
        df_news_working['Institution'] = df_news_working['source_name']

        # extract year properly
        df_news_working["Year"] = df_news_working.apply(lambda row : get_year_from_publishedAt(row['publishedAt']), axis=1)

        # Define what type of literature
        df_news_working["Source"] = 'news'

        # Clean description to remove links
        df_news_working["description"] = df_news_working.apply(lambda row : remove_links(row['description']), axis=1)
        df_news_working["description"] = df_news_working.apply(lambda row : find_200_char_limit(row['description']), axis=1)
        df_news_working["content"] = df_news_working.apply(lambda row : remove_links(row['content']), axis=1)
        df_news_working["content"] = df_news_working.apply(lambda row : find_200_char_limit(row['content']), axis=1)

        # find which one is longer description or content
        df_news_working["usecase"] =df_news_working.apply(lambda row : find_column_with_more_unique_words(row['description'],row['content']), axis=1)

        # Change names of columns to match pubmed output
        df_news_working = df_news_working.rename(columns={'title': 'Title',
                                'usecase': 'Text',
                               'url': 'Unique_id',
                               'source_name': 'Published By',
                               'publishedAt': 'Published Date',
                               'Year': 'Year',
                               'Source':'Source Type'
                               })
        # rearrange columns to match pubmed output
        df_news_working = df_news_working[['Title', 'Text', 'Published By', 'Published Date', 'Year', 'Unique_id', 'Institution','Source Type']]
        st.session_state.df_news = df_news_working
        st.session_state.news_df_created = True

        st.experimental_rerun()
    else:
        df_news_working = st.session_state.df_news

        #st.subheader('Parse elastic search news articles')




        st.subheader('Output from Elastic Search for news')
        # show output
        st.write(df_news_working)

        # convert to json
        file_news = df_news_working.to_json()


        # save funcitonality
        if file_news is not None:
            st.write('###')
            st.write('### Download as json file')
            st.write(' It may freeze temporarily after entering name for file')

            write_filename_text_news = st.text_input('Enter name for file to download file and press Enter', key = 'write_filename_text_news')
            if write_filename_text_news == "":
                write_filename_text_news = 'output'
            st.download_button(
                label="Download output as json",
                data=file_news,
                file_name=write_filename_text_news+'.json',
                mime='text/json'
            )


st.write("")
st.write("")
st.write("")
st.write("")
st.subheader('Pull Education Resources Information Center (ERIC) from Elastic Search')
st.write(' This database contains journal articles and grey literature data. There may also be an overlap between research documents.')
if 'eric_elastic_button' not in st.session_state:
    st.session_state.eric_elastic_button = False

if "eric_df_created" not in st.session_state:
    st.session_state.eric_df_created = False

if "eric_df" not in st.session_state:
    st.session_state.eric_df = False


eric_elastic_button = st.button('Click to pull ERIC from Elastic Search', key = 'eric_elastc_button')

if eric_elastic_button or st.session_state.eric_elastic_button:
    st.session_state.eric_elastic_button = True

    if st.session_state.eric_df_created == False:
        with st.spinner(' Pulling ERIC from Elastic search'):
            df_eric = get_data_from_elastic("search-eric")

        df_eric_working = df_eric[['title', 'description', 'publisher','publicationdateyear','id']]
        df_eric_working['Source Type'] = 'grey'
        df_eric_working['publicationdateyear'] = df_eric_working['publicationdateyear'].astype(int)
        df_eric_working['publicationdateyear'] = df_eric_working['publicationdateyear'].astype(str)
        df_eric_working['Year'] = df_eric_working['publicationdateyear']

        df_eric_working['publisher'] = str(df_eric_working['publisher'])
        df_eric_working["publisher"] = df_eric_working.apply(lambda row : fix_missing_published_by(row["publisher"]), axis=1)
        df_eric_working["publisher"] = df_eric_working.apply(lambda row : fix_publisher_eric(row['publisher']), axis=1)
        df_eric_working["publisher"] = df_eric_working.apply(lambda row : remove_whitespace(row['publisher']), axis=1)

        df_eric_working['Institution'] = df_eric_working['publisher']

        df_eric_working = df_eric_working.rename(columns={'title': 'Title',
                                'description': 'Text',#
                               'id': 'Unique_id',
                               'publisher': 'Published By',
                               'publicationdateyear': 'Published Date',
                               'Year': 'Year',
                               })

        df_eric_working = df_eric_working[['Title', 'Text', 'Published By', 'Published Date', 'Year', 'Unique_id', 'Institution','Source Type']]
        #df_eric_working


        st.session_state.df_eric = df_eric_working
        st.session_state.eric_df_created = True

        st.experimental_rerun()

    else:
        df_eric_working = st.session_state.df_eric

        st.subheader('Output from Elastic Search for ERIC')
        df_eric_working

        # convert to json
        file_eric = df_eric_working.to_json()

    # save funcitonality
        if file_eric is not None:
            st.write('###')
            st.write('### Download as json file')
            st.write(' It may freeze temporarily after entering name for file')

            write_filename_text_eric = st.text_input('Enter name for file to download file and press Enter', key = 'write_filename_text_eric')
            if write_filename_text_eric == "":
                write_filename_text_eric = 'output'


            st.download_button(
                label="Download output as json",
                data=file_eric,
                file_name=write_filename_text_eric+'.json',
                mime='text/json'
            )
