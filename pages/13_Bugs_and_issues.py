import streamlit as st

st.header(' Bugs/ Limitations and Issues within app')

st.write('Both simple and complex initial model pages show errors, these go away once the button is clicked')
st.write("Both simple and complex don't have the option to rerun the model without reloading the entire app")

st.write("pages can't be switched once a process has started on a page, the user must wait unitl it completes before moving to another page")

st.write("Word cloud output isn't saved, might not be an issue due to relatively fast reloading")

st.write('Some publications have dates for 2023, these are minimal but retained for future use, especially so close to the new year. At this point, it mainly affects scientific publicatios')
