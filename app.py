import streamlit as st
import json
from cv_formatting import json_to_cv
import os

st.set_page_config(page_title="ORCID CV Generator", layout="centered")

st.title("ORCID CV Generator")
st.write("Convert your ORCID profile JSON to a formatted Markdown CV")

uploaded_file = st.file_uploader("Upload your ORCID JSON file", type=['json'])

if uploaded_file:
    try:
        json_data = json.load(uploaded_file)
        markdown_cv = json_to_cv(json_data)
        
        # Display the markdown
        st.markdown("## Preview")
        st.markdown(markdown_cv)
        
        # Download buttons
        st.download_button(
            label="Download CV as Markdown",
            data=markdown_cv,
            file_name="cv.md",
            mime="text/markdown"
        )
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
