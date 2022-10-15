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
# Get data from ElastiSearch
es = Elasticsearch(
    cloud_id="WHS:YXVzdHJhbGlhLXNvdXRoZWFzdDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGNhYTExYzViNzQ3YjQwMzViZWFhNzQ1MTcwY2EwOWZlJDZkOWQxNzg1ZjM1MDQxMDdhOTcxMWYyMWU5YjE3ZmQx",
    basic_auth=("elastic", "BnV9bouQp2Pbksh0Zla8Ow78")
)

def fix_missing_published_by(text):
    if len(text)<3:
        text = 'unknown'

    return text

# Put into database
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


st.header('Parse elastic search news articles')


st.write(' The newsapi package is used to scrape various news articles from a variety of major news outlets on the web which are uploaded into Elastic Search.')
st.write(' The Free model used for this prototype is limited to the first ~200 characters.')
st.write(' As this is a proof of concept, we only aim to prove the potential usage of this functionality.')
st.write("")

st.subheader('Output from Elastic Search')
# show output
st.write(df_news_working)

# convert to json
file = df_news_working.to_json()


# save funcitonality
if file is not None:
    st.write('###')
    st.write('### Download as json file')
    st.write(' It may freeze temporarily after entering name for file')

    write_filename_text = st.text_input('Enter name for file to download file and press Enter')
    if write_filename_text == "":
        write_filename_text = 'output'


    st.download_button(
        label="Download output as json",
        data=file,
        file_name=write_filename_text+'.json',
        mime='text/json'
    )

###################
# Add additional database - work in progress
###################
# Put into database
#df_eric = get_data_from_elastic("search-eric")
#df_eric_working = df_eric[['title', 'description', 'publisher','publicationdateyear','id']]
#df_eric_working['Source Type'] = 'grey'
#df_eric_working['Year'] = df_eric_working['publicationdateyear']
#df_eric_working['Institution'] = str(df_eric_working['publisher'])

#df_news_working["Institution"] = df_news_working.apply(lambda row : fix_publisher_eric(row['Institution']), axis=1)
#df_news_working["publisher"] = df_news_working.apply(lambda row : fix_missing_published_by(row['publisher']), axis=1)
#df_eric_working = df_eric_working.rename(columns={'title': 'Title',
#                        'description': 'Text',#
#                       'id': 'Unique_id',
#                       'publisher': 'Published By',
#                       'publicationdateyear': 'Published Date',
#                       'Year': 'Year',
#                       })

#df_eric_working = df_eric_working[['Title', 'Text', 'Published By', 'Published Date', 'Year', 'Unique_id', 'Institution','Source Type']]



#df_eric_working
