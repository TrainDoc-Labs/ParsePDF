import streamlit as st
import pymupdf4llm
import tempfile
import os

# Set page layout to wide
st.set_page_config(page_title="ParsePDF Pro", layout="wide")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .reportview-container { background: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 ParsePDF")
st.markdown("Easily convert your PDFs into clean, structured Markdown.")

# Sidebar for controls
with st.sidebar:
    st.header("Upload & Settings")
    uploaded_file = st.file_uploader("Select a PDF", type="pdf")
    ignore_imgs = st.toggle("Ignore images", value=True)
    convert_btn = st.button("Convert to Markdown", type="primary")

# Main display area
if uploaded_file and convert_btn:
    with st.status("Processing your document...", expanded=True) as status:
        # ... [Your logic for tempfile and pymupdf4llm here] ...
        # (Assuming md_text is retrieved successfully)
        
        status.update(label="Done!", state="complete", expanded=False)
        
    # Use tabs for a better UI experience
    tab1, tab2 = st.tabs(["Preview", "Raw Code"])
    
    with tab1:
        st.markdown(md_text)
        
    with tab2:
        st.code(md_text, language="markdown")
        
    st.download_button("Download .md File", md_text, "document.md", "text/markdown")
