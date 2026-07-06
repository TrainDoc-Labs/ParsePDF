import streamlit as st
import pymupdf4llm
import tempfile
import os

st.title("ParsePDF: PDF to Markdown")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file and st.button("Convert"):
    # Create a secure temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        # Perform conversion
        md_text = pymupdf4llm.to_markdown(
            tmp_path, 
            ignore_images=True, 
            header=False, 
            footer=False, 
            show_progress=True
        )
        st.success("Conversion successful!")
        
        # Display the output
        st.markdown(md_text)
        
        # Add the download button
        st.download_button(
            label="Download Markdown",
            data=md_text,
            file_name="converted_document.md",
            mime="text/markdown"
        )
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Ensure cleanup happens even if an error occurs
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
