import streamlit as st
import pandas as pd
import json

st.header('Input multiple jsons and emrge into one larger file')
st.subheader('Warning message disappears once files are uploaded')

# upload files
uploaded_json_files = st.file_uploader("Upload json files",type=['json'], accept_multiple_files=True)

#uploaded_json_files
final_merged_df = pd.DataFrame()


# loop over uploaded json files
for uploaded_file in uploaded_json_files:
    # load in as json
    json_file = json.load(uploaded_file)
    # convert to df
    df_working = pd.DataFrame(json_file)
    # merge/concat - they should all have column names
    final_merged_df = pd.concat([final_merged_df,df_working], axis = 0)

# reset index
final_merged_df.reset_index(drop=True, inplace=True)

# save functionality
if uploaded_file is not None:
    st.write('###')
    st.write('### Download as json file')

    write_filename_text = st.text_input('Enter name for file to download file and press Enter')
    if write_filename_text == "":
        write_filename_text = 'output'


    st.download_button(
        label="Download output as json",
        data=final_merged_df.to_json(),
        file_name=write_filename_text+'.json',
        mime='text/json'
    )
