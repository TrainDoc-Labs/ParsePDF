import streamlit as st
import pymupdf4llm
import tempfile
import os

# Set page layout to wide
st.set_page_config(page_title="ParsePDF Pro", layout="wide")

st.title("📄 body = ParsePDF")

# Sidebar for controls
with st.sidebar:
    st.header("Upload & Settings")
    uploaded_file = st.file_uploader("Select a PDF", type="pdf")
    
    # Checkboxes for toggling header/footer
    include_header = st.checkbox("Include headers", value=False)
    include_footer = st.checkbox("Include footers", value=False)
    
    convert_btn = st.button("Convert to Markdown", type="primary")

# Main display area
if uploaded_file and convert_btn:
    # Use a status container to show progress
    with st.status("Processing your document...", expanded=True) as status:
        # Create a secure temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Perform the conversion using the toggle values
            md_text = pymupdf4llm.to_markdown(
                tmp_path, 
                ignore_images=True, 
                header=include_header, 
                footer=include_footer
            )
            
            status.update(label="Done!", state="complete", expanded=False)
            
            # Use tabs for a better UI experience
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
            # Clean up the temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


