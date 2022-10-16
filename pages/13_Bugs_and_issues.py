import streamlit as st

st.header('Bugs/ Limitations and Issues within app')

st.write('Access to documents in Elastic Search must be access within the source code. There is currently no option to search the database within this app.')
st.write('Some pages default to showing errors. This is specifically mentioned on relevant pages along with how to proceed')
st.write("Pages can't be switched once a process has started on a page, the user must wait unitl it completes before moving to another page")
st.write("The simple model word cloud doesn't have an inbuilt option to save. Saving must be right clicked on each image to save")
st.write('Some publications have dates for 2023, these are minimal but retained for future use, especially so close to the new year. At this point, it mainly affects scientific publicatios')
st.write('If a model is uploaded to the complex model, the dataframe must still be calculated which takes time. This could be fixed by also suploading a previously saved dataframe however this adds complexity to the model memory flow as was too difficult to implement in the time given.')
st.write('There is not an option to include more complex language embeddings which can improve results.  These were initally included but as they increased time taken for a model to train, they were removed and have not been added back in.')
st.write('There were occassional issues when uploading a model after a model has already ran. While care has been taken to ensure all components of the initial memory are removed from memory, its possible that a user may break the logic. In this case, restarting the program and uploading the model should result in the intented outcomes.')
st.write("The work in progress page has an operational PyLDAVIS which is a widely used visualisation package used for topic modelling using LDA methods. Due to the streamlit operating process, it doesn't so is left out. Updates to streamlit or deployment on another application may alleviate this issue ")
st.write('Topics are not labelled in any part of this project. A model was implemented that was trained for this task (https://huggingface.co/cristian-popa/bart-tl-ng) but it performed poorly (heat, workers, burn gave topic name of solenoid-coated steel alloy)')
# In future add embedding options
