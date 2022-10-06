import streamlit as st
import string
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector
import pandas as pd


def word_length(text):
  words = text.split()
  return len(words)

def lemmatise_(text):
    doc_ = sp(text)
    output = " ".join([token.lemma_ for token in doc_ if len(token.lemma_) >2])
    return output


def find_journal_information(text):
    journal_info = text[text.find(" "):]

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
    study_name = text.translate(str.maketrans('', '', string.punctuation))
    if study_name.endswith('.'):
        study_name = study_name[:-1]
    return study_name


def find_doi(text):
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
    start = text.find('PMID')
    pmid_int = text[start+6:]

    if " " in pmid_int:
        #print(pmid_int, pmid_int.find(" "))
        pmid = pmid_int[:pmid_int.find(" ")]
    else:
        pmid = pmid_int

    return pmid

def get_institution_info(text):
    institutions = text[5+text.find('Author information')+len('Author information '):]
    institutions = institutions.replace('.', "")

    if "(2)" in institutions:
        institutions = institutions[:institutions.find("(2)")]

    #st.write('institutions',institutions)
    return institutions
# not using
def check_language(text):

    # Run language model to skip non English textx
    doc_1 = nlp_model_lang_dect(text)
    language = doc_1._.language

    # what language is it
    langauge_out = language['language']


    return langauge_out

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

output_list = []
num_words = 0
number_of_texts = 0
num_records_skipped = 0

uploaded_files = st.file_uploader("", type = ['txt'])

if uploaded_files is not None:

    st.write('### Results of parsing txt file')

    if uploaded_files.type == "text/plain":

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

            # split txt file by new line
            paragraphs = paper.split('\r\n\r\n')

            # Get relevant fields.
            journal_info = find_journal_information(paragraphs[0])
            study_name = title_of_paper(paragraphs[1])
            date_of_publication = find_date_initial_search(journal_info)
            #institution_information = get_institution_info(paragraphs[i])
            find_text_outputs = find_text(paper)
            main_text = find_text_outputs[0]
            #langauge_out = check_language(main_text)
            doi =  find_text_outputs[1]
            pmid = find_text_outputs[2]
            institution_information = find_text_outputs[3]

            # fasdter to save as dict and append
            paper_info = {
            'Title': study_name,
            #'Language':langauge_out,
            'Text': main_text,
            "Journal Information": journal_info, # source
            'Published':date_of_publication,
            'PMID':pmid,    # uuid? /weburl
            'DOI':doi,
            'Institutions':institution_information
            }

            # append
            output_list.append(paper_info)

    # save to pandas df
    df_final = pd.DataFrame.from_dict(output_list)

    # show exmaple df
    st.write(df_final)

    # convert to json
    file = df_final.to_json()

    if file is not None:
        st.write('###')
        st.write('### Download as json file')
        st.download_button(
            label="Download output as json",
            data=file,
            file_name='sample_df.json',
            mime='text/json'
        )
