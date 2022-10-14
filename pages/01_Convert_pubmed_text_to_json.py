import streamlit as st
import string
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector
import pandas as pd

# helper functions
def word_length(text):
    # take some text and split into individual words
    # return the list of words

  words = text.split()
  return len(words)

def lemmatise_(text):
    # Perform lemmatisation of input text word by word using spacy lemmatization
    # Join the now lemmatized words baack into a list
    doc_ = sp(text)
    output = " ".join([token.lemma_ for token in doc_ if len(token.lemma_) >2])
    return output

def find_journal_information(text):
    # Find journal info from text
    # Very specific to Pubmed txt output
    journal_info = text[text.find(" "):]

    # If Doi in text, fextract it
    if 'doi' in journal_info:
        journal_info = journal_info[:journal_info.find('doi')]

    return journal_info


def find_date_initial_search(journal_info):
    # extract years and month from journal info

    if journal_info.find(" 19") != -1:
        start_point = journal_info.find(" 19")
        date_of_publication = journal_info[start_point+1:start_point+9]

        if date_of_publication[2] == "." or date_of_publication[2] == ";":
            date_of_publication = 'unknown'
        elif (len(date_of_publication) < 8) or (date_of_publication[4] != " "):
            date_of_publication = date_of_publication[0:4] + ' unk'


    elif journal_info.find(" 20") != -1:
        start_point = journal_info.find(" 20")
        date_of_publication = journal_info[start_point+1:start_point+9]

        if date_of_publication[2] == "." or date_of_publication[2] == ";":
            date_of_publication = 'unknown'
        elif (len(date_of_publication) < 8) or (date_of_publication[4] != " "):
            date_of_publication = date_of_publication[0:4] + ' unk'

    else:
        date_of_publication = 'unknown'

    if len(date_of_publication) >10: # something weird
        date_of_publication = 'unknown'

    return date_of_publication


def title_of_paper(text):
    # Get paper name and remove punctuation
    study_name = text.translate(str.maketrans('', '', string.punctuation))
    if study_name.endswith('.'):
        study_name = study_name[:-1]
    return study_name


def find_doi(text):

    # Get oi from another column if there is an erro with initial parsing
    doi_start = text.find("10.")
    doi_int = text[doi_start:]

    doi_end_space = doi_int.find(" ")
    doi_end_line_break = doi_int.find("\r\n")

    if doi_end_space == '-1':
        # there is no space in doi
        doi_end = doi_end_line_break

    elif doi_end_line_break == '-1':

        # there is no line break in doi
        doi_end = doi_end_space

    else: # both space and line break occur
        # check which occurs first
        if doi_end_space < doi_end_line_break:
            doi_end = doi_end_space
        else:
            doi_end = doi_end_line_break

    doi = doi_int[:doi_end]
    doi = doi[:doi.find(" ")]

    return doi

def find_pmid(text):
    # extract PMID
    start = text.find('PMID')
    pmid_int = text[start+6:]

    if " " in pmid_int:
        #print(pmid_int, pmid_int.find(" "))
        pmid = pmid_int[:pmid_int.find(" ")]
    else:
        pmid = pmid_int

    return pmid

def get_institution_info(text):
    # Get the research institution
    institutions = text[5+text.find('Author information')+len('Author information '):]
    institutions = institutions.replace('.', "")

    if "(2)" in institutions:
        institutions = institutions[:institutions.find("(2)")]

    #st.write('institutions',institutions)
    return institutions

def find_text(paper):

    #find longest parapgraph, likely to be main text
    longest_paragraph_length = 0
    longest_paragraph_index = 0
    doi_ = ""
    pmid_ = ""
    # split txt file by new line
    paragraphs = paper.split('\r\n\r\n')
    institution_information_ = ""
    for i in range(0,len(paragraphs)):

        # PMID and DOI
        #st.write(paragraphs[i])

        if 'doi' in paragraphs[i].lower() and i >2:
            #st.write('doi found')
            doi_ = find_doi(paragraphs[i])

        if 'PMID' in paragraphs[i] and i >2:
            #st.write('pmid found')
            pmid_ = find_pmid(paragraphs[i])

        if 'Author information' in paragraphs[i]:

            institution_information_ =get_institution_info(paragraphs[i])

        # look for longest paragraph by length, likey to be main text, skip if author name
        if len(paragraphs[i]) > longest_paragraph_length:# or 'Author information' in paragraphs[i] == False or 'Author information:' in paragraphs[i] == False:

            if 'Author information' in paragraphs[i]:
                continue
            #i#nstitution_information_ = 'unknown'
            #st.write('institution_information_ 2', institution_information_)
            longest_paragraph_index = i
            longest_paragraph_length = len(paragraphs[i])

            if len(paragraphs[longest_paragraph_index].split(" ")) <= 50:
                continue

            #if institution_information_ is None:
            #    institution_information_ = 'unknown'

    return paragraphs[longest_paragraph_index].replace('\r\n', ""), doi_, pmid_, institution_information_

def text_validity(text):
    words = text.split()
    if len(words) <30 or len(words) > 500:
        return "skip due to length"
    else:
        return text

def title_valid(text):
    words = text.split()
    if len(words) > 30:
        return "skip due to length"
    else:
        return text

def publish_validity(text):
    if len(text) >10:
        return "skip due to length"
    else:
            return text

def publish_weird_format(text, orig):
    if 'unknown' in text or '19:1' in text or '19:S' in text or '198-' in text:

        if ' 20' in text:

            year_info = text
            year_start = year_info.find(' 20')
            year_end = year_start + 9#len(' 2022 Apr')
            year_proper = year_info[year_start:year_end]

            return year_proper

        elif '19' in text:

            year_info = text
            year_start = year_info.find(' 19')
            year_end = year_start + 9
            year_proper = year_info[year_start:year_end]
            #text = year_proper

            return year_proper

        else:
            return orig
            pass
    else:
        return orig

def get_year_from_published(text):
    text = text.strip()
    return text[0:4]

st.write("# Upload search results from Pubmed as a txt file")

st.markdown(
    """
    ### Expected format is the result of the following search method
    - Enter keywords into PubMed search engine (https://pubmed.ncbi.nlm.nih.gov/)
    - Click on save
    - In seleciton drop down menu, select All results
    - In format drop down menu, select Abstract (text)


    Upload the file into the uploading widget below
"""
)

# Define starting values and empty list
output_list = []
num_words = 0
number_of_texts = 0
num_records_skipped = 0

st.write("")
st.subheader('Upload file')
uploaded_files = st.file_uploader("", type = ['txt'])

# Proceed once file as been uploadded
if uploaded_files is not None:

    st.write('### Results of parsing txt file')

    # Check type of file uploaded is valid
    if uploaded_files.type == "text/plain":

        # convert to raw format for extraction
        raw_text = str(uploaded_files.read(),"utf-8")

        # split papers as they are seperated by 3 empty lines
        paper_info = raw_text.split('\r\n\r\n\r\n')

        # loop over papers after they've been split
        for paper in paper_info:

            # set defualts in case of failure
            study_name = 'unknown'
            #langauge_out = 'unknown'
            journal_info  = 'unknown'
            date_of_publication  = 'unknown'
            pmid  = 'unknown'
            doi  = 'unknown'
            institution_information_ = 'unknown'
            year = 'unknown'

            # split txt file by new line
            paragraphs = paper.split('\r\n\r\n')

            # Get relevant fields.
            journal_info = find_journal_information(paragraphs[0])

            # Get study name
            study_name = title_of_paper(paragraphs[1])
            study_name = title_valid(study_name)

            # Get data by checking multiple functions
            date_of_publication = find_date_initial_search(journal_info)
            date_of_publication = publish_validity(date_of_publication)
            date_of_publication = publish_weird_format(journal_info, date_of_publication)

            # get resuls of text output - main text, pmid and doi
            find_text_outputs = find_text(paper)

            # Set main text anccheck it fits within length specs to remove incorrcet parsing
            main_text = find_text_outputs[0]
            main_text = text_validity(main_text)

            # Get dpo
            doi =  find_text_outputs[1]

            # check DOI is valid else set to unknown
            if len(str(doi))<3:
                doi ='unknown'

            # Get PMID
            pmid = find_text_outputs[2]

            #Get instituitona name and check if valid else set to unknown
            institution_information = find_text_outputs[3]
            if len(str(institution_information))<3:
                institution_information ='unknown'

            # Get year from Published Date
            year = get_year_from_published(date_of_publication)

            # Faster to save as dictionary and append
            paper_info = {
            'Title': study_name,
            'Text': main_text,
            "Published By": journal_info, # source
            'Published Date':date_of_publication,
            'Year':year,
            'Unique_id':doi,
            'Institution':institution_information,
            'Source Type': 'academic'
            }

            # append to list
            output_list.append(paper_info)

    # save to pandas df
    df_final = pd.DataFrame.from_dict(output_list)

    # show example df
    st.write(df_final)

    # convert to json
    file = df_final.to_json()

    # saving functionality
    if file is not None:
        st.write('###')
        st.write('### Download as json file')

        write_filename_text = st.text_input('Enter name for file to download file and press Enter')
        if write_filename_text == "":
            write_filename_text = 'output'


        st.download_button(
            label="Download output as json",
            data=file,
            file_name=write_filename_text+'.json',
            mime='text/json'
        )
