import streamlit as st
import pymupdf4llm
import tempfile
import os

# Set page layout to wide
st.set_page_config(page_title="ParsePDF Pro", layout="wide")

st.title("📄 ParsePDF")

with st.sidebar:
    st.header("Upload & Settings")
    uploaded_file = st.file_uploader("Select a PDF", type="pdf")
    include_header = st.checkbox("Include headers", value=False)
    include_footer = st.checkbox("Include footers", value=False)
    convert_btn = st.button("Convert to Markdown", type="primary")

if uploaded_file and convert_btn:
    with st.status("Processing your document...", expanded=True) as status:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # pymupdf4llm returns pure Markdown
            md_text = pymupdf4llm.to_markdown(
                tmp_path, 
                ignore_images=True, 
                show_progress=False, # Optional: suppresses console prints
                page_chunks=False,
                hdr_footers=include_header # Note: Ensure parameter names match your version
            )
            
            # NOTE: Removed BeautifulSoup usage here as it destroys Markdown
            
            status.update(label="Done!", state="complete", expanded=False)
            
            tab1, tab2 = st.tabs(["Preview", "Raw Code"])
            
            with tab1:
                st.markdown(md_text)
                
            with tab2:
                st.code(md_text, language="markdown")
                
            st.download_button(
                label="Download .md File", 
                data=md_text, 
                file_name="document.md", 
                mime="text/markdown"
            )

        except Exception as e:
            status.update(label="Conversion failed!", state="error", expanded=True)
            st.error(f"An error occurred: {e}")
            
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
