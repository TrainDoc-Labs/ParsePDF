import streamlit as st
import pymupdf4llm
import tempfile
import os

st.title("ParsePDF")

# Initialize session state to store the conversion result
if "md_text" not in st.session_state:
    st.session_state.md_text = None

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if st.button("Convert") and uploaded_file:
    with st.status("Converting...", expanded=True) as status:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Assign to session state instead of a local variable
            st.session_state.md_text = pymupdf4llm.to_markdown(tmp_path)
            status.update(label="Complete!", state="complete", expanded=False)
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

# Only attempt to display if the variable exists in session state
if st.session_state.md_text:
    st.success("Conversion successful!")
    st.markdown(st.session_state.md_text)
    st.download_button(
        label="Download Markdown",
        data=st.session_state.md_text,
        file_name="converted.md",
        mime="text/markdown"
    )
