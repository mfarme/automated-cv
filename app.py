import streamlit as st
import json
from cv_formatting import json_to_cv
import os
#import beautifulsoup4
from bs4 import BeautifulSoup
from orcid_api import get_orcid_profile, is_valid_orcid
from md_to_doc import convert_to_docx

st.set_page_config(page_title="ORCID CV Generator", layout="centered")

st.title("ORCID CV Generator")
st.write("Convert your ORCID profile to a formatted CV")

orcid_id = st.text_input("Enter your ORCID iD (format: XXXX-XXXX-XXXX-XXXX)")

if orcid_id:
    if is_valid_orcid(orcid_id):
        profile = get_orcid_profile(orcid_id)
        if profile:
            markdown_cv = json_to_cv(profile)
            
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
            
            # Convert markdown to DOCX
            md_file_path = "cv.md"
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_cv)
            
            docx_path = convert_to_docx(md_file_path, ".")
            
            with open(docx_path, "rb") as docx_file:
                st.download_button(
                    label="Download CV as DOCX",
                    data=docx_file,
                    file_name="cv.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            st.error("Failed to fetch ORCID profile.")
    else:
        st.error("Invalid ORCID iD format.")
