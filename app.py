import streamlit as st
from docling.document_converter import DocumentConverter
import tempfile
import os

st.set_page_config(page_title="ParsePDF Pro", layout="wide")
st.title("📄 ParsePDF with Docling")

# 1. Cache the converter so it doesn't reload on every interaction
@st.cache_resource
def get_converter():
    return DocumentConverter()

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Select a PDF", type="pdf")
    convert_btn = st.button("Convert to Markdown", type="primary")

if uploaded_file and convert_btn:
    with st.status("Processing with Docling...", expanded=True) as status:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # 2. Use Docling to convert
            converter = get_converter()
            result = converter.convert(tmp_path)
            clean_md_text = result.document.export_to_markdown()
            
            status.update(label="Done!", state="complete", expanded=False)
            
            tab1, tab2 = st.tabs(["Preview", "Raw Code"])
            with tab1:
                st.markdown(clean_md_text)
            with tab2:
                st.code(clean_md_text, language="markdown")
                
            st.download_button("Download .md", clean_md_text, "document.md")

        except Exception as e:
            status.update(label="Failed!", state="error", expanded=True)
            st.error(f"Error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
