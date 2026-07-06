import streamlit as st
from markitdown import MarkItDown
import tempfile
import os

st.set_page_config(page_title="ParsePDF Pro", layout="wide")
st.title("📄 ParsePDF with MarkItDown")

# Initialize MarkItDown
md_tool = MarkItDown()

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Select a file", type=["pdf", "docx", "pptx", "xlsx"])
    convert_btn = st.button("Convert to Markdown", type="primary")

if uploaded_file and convert_btn:
    with st.status("Converting...", expanded=True) as status:
        # Save uploaded file to temp path
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Conversion happens here
            result = md_tool.convert(tmp_path)
            clean_md_text = result.text_content
            
            status.update(label="Done!", state="complete", expanded=False)
            
            st.markdown(clean_md_text)
            st.download_button("Download .md", clean_md_text, "document.md")

        except Exception as e:
            status.update(label="Failed!", state="error", expanded=True)
            st.error(f"Error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
