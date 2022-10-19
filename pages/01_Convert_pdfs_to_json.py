import streamlit as st
import json
import re
import pandas as pd
import string
import spacy
import math
import tika
tika.initVM() # new
from tika import parser
import uuid
from os import listdir
from os.path import isfile, join


sp = spacy.load('en_core_web_sm')
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop = stopwords.words('english')

def remove_numbers_from_text(text):
    # remove numbers from text using regex
    pattern = r'[0-9]'
    no_numbers = re.sub(pattern, '', text)
    return no_numbers

def check_http(text):
    # check if http in text used for another alter function
    if 'http' in text:
        return True
    else:
        return False

def remove_https(text):
    # recusrive funciton to remove all https link in text
    if 'http' in text:

        # find start of https
        html_start = text.find('http')
        temp = text[html_start:]
        space_after_html = temp.find(" ")

        # check its not the ned of the text which has the index -1
        if space_after_html == -1:
            space_after_html = len(text)

        # start of text to html    #loction of first  space after hetml - end of link
        result = text[:html_start]+text[html_start+space_after_html:]

        # Repeat until all finished

        if 'http' in result:
            result = remove_https(result)
            return result
        else:
            return result

    else:
        # no http return original text
        return text

def remove_www(text):
    # same as above but with www
    if 'www' in text:
        #sprint('initial loop')

        # find start of www
        html_start = text.find('www')
        temp = text[html_start:]
        space_after_html = temp.find(" ")

        if space_after_html == -1:
            space_after_html = len(text)

        # start of text to www    #loction of first space after www
        result = text[:html_start]+text[html_start+space_after_html:]

        # recursive

        if 'www' in result:
            result = remove_https(result)
            return result
        else:
            return result

    else:
        return text

def remove_mailto(text):
    # same as before but with mailto
    if 'mailto' in text:
        #sprint('initial loop')

        # find start of mailto
        html_start = text.find('mailto')
        temp = text[html_start:]
        space_after_html = temp.find(" ")


        if space_after_html == -1:
            space_after_html = len(text)

        # start of text to mailto    #loction of first space after mailto , end of link
        result = text[:html_start]+text[html_start+space_after_html:]

        # recursive
        if 'mailto' in result:

            result = remove_https(result)
            return result
        else:
            return result

    else:
        return text

st.header('Upload multiple pdf files')
st.write("")
st.write("This page allows for the option to load multiple pdfs at once. The text will be extracted stored into a dataframe. Chunking of 250 words also occurs. This is necessary otherwise there is arisk that the models may run into memory errors.")
st.write("http, www and mailto links are removed as they are don't offer any value to the modelling process.")
st.write('Numbers are also removed as they only contribute to noise.')

st.write("")
st.subheader('Upload pdf document')
# check file is uploaded
if 'proceed' not in st.session_state:
    uploaded_pdf_files = st.file_uploader("",type=['pdf'], accept_multiple_files=True)

    # Create empty list
    output_list = []

    # loop over all uploaded files
    for uploaded_file in uploaded_pdf_files:

         # set basics
        Title = 'blank'
        Text = "blank"
        Journal_information = 'blank'
        Published = 'unknown'
        PMID = 'unknown'
        unique = uuid.uuid4()
        Institution = 'unknown'


        # do parsing here

        # Get Title from file name
        Title = str(uploaded_file)
        Title = Title[Title.find("-")+1:]
        Title = Title[:Title.find(".pdf"):]

        # get metadata - has info on dates and text
        metadata = parser.from_file(uploaded_file)

        # Parse metadata to get text
        Text = metadata['content'].replace("\n","")
        # convert ot lower case
        Text = Text.strip().replace('..',"").replace('\xa0'," ").lower()
        # run through http, www and mailto removal functions
        Text = remove_https(Text)
        Text = remove_www(Text)
        Text = remove_mailto(Text)

        # replace phrases of companies, way more tht could be added here
        Text = Text.replace('deloitte touche tohmatsu'," ")
        Text = Text.replace('mckinsey & company', " ")
        Text = Text.replace('mckinsey and company', " ")
        Text = Text.replace("all rights reserved", " ")

        # Perform additional cleaning in case previous effort missed something
        Text = " ".join([word for word in Text.split() if '.com' not in word])
        Text = " ".join([word for word in Text.split() if 'www' not in word])
        Text = " ".join([word for word in Text.split() if 'copyright' not in word])
        Text = " ".join([word for word in Text.split() if '©' not in word])

        # Get journal/publisher information
        Journal_information = str(uploaded_file)
        Journal_information = Journal_information[:Journal_information.find('-')]
        Journal_information = Journal_information[Journal_information.find('name=')+6:]

        # Try tto find date else set to unknown
        try:
            Published = metadata['metadata']['Last-Modified'][:4] # can get date as well
        except:
            Published = 'unknown'

        # # needed to match formatting of pubmed output
        Institution = Journal_information

        #chunk long pdf text

        # if text longer than 250. break into 250 word chunks
        # might not be a good way to go, but models work better with more data
        if len(Text.split())>300:

            # how many chunks of 300 words can be made
            for i in range(0,math.ceil(len(Text.split())/300)):

                # lopo over chunks
                text_start = 300*i #(0, 300, 600, 900 etc)
                text_finish = 300*(i+1) #(300, 600, 900, 1200 etc)

                if text_finish > len(Text.split()): # make sure to not go o far
                    text_finish = len(Text.split())



                # # break into 300 word chunk
                Text_chunk = Text.split()[text_start:text_finish]

                # output is list ,join back to string e.g. ['this', ' is', ,'a', 'list'] -> 'this is a list'
                Text_chunk = " ".join([word for word in Text_chunk])

                # set values
                pdf_info = {
                        'Title': Title+"_chunk_"+str(i), # add chunk value to title
                        'Text': str(Text_chunk),
                        "Published By": Journal_information,
                        'Published Date':Published,
                        'Year' : Published,
                        'Unique_id':str(unique)+"_chunk_"+str(i),# add chunk value to unique to keep it unique
                        'Institution':Journal_information,
                        'Source Type': 'grey'
                        }

                # append to list
                output_list.append(pdf_info)



        else:

            pdf_info = {
                    'Title': Title,
                    'Text': str(Text),
                    "Published By": Journal_information,
                    'Published Date':Published,
                    'Year' : Published,
                    'Unique_id':str(unique),
                    'Institution':Journal_information,
                    'Source Type': 'grey'
                    }

            # append to list
            output_list.append(pdf_info)

    # Copleted parsing pdfs, put output into a pandas dataframe
    df_final = pd.DataFrame.from_dict(output_list)

    # Using multiple uploaded has weird functionality, this gets around it

    # check shape is not 0, it has data
    if int(df_final.shape[0]) >0:
        # set session state values
        st.session_state.df_final = df_final
        st.session_state.proceed = True
        # restart to start at next section
        st.experimental_rerun()


else:
    # everything has been aprsed and loaded

    # load in df from session state
    df_final = st.session_state.df_final

    st.subheader('Resulting DataFrame')
    st.write(df_final)

    # convert to json


    file = df_final.to_json()

    if file is not None:
        st.write('###')
        st.write('### Download as json file')

        write_filename_text = st.text_input('Enter name for file to download file and press Enter', key = 'write_filename_text pdfs asjdhaisudhaiufhiuhfiuah')
        if write_filename_text == "":
            write_filename_text = 'output'


        st.download_button(
            label="Download output as json",
            data=file,
            file_name=write_filename_text+'.json',
            mime='text/json'
        )
