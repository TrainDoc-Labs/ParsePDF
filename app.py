import streamlit as st
import pdfplumber
import tempfile
import os

st.set_page_config(page_title="PDF to Markdown", layout="wide")
st.title("📄 PDF to Markdown (Table-Aware)")

uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    if st.sidebar.button("Convert"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            markdown_output = []
            
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    # 1. Extract tables first
                    tables = page.extract_tables()
                    text = page.extract_text()
                    
                    # 2. Convert tables to Markdown format
                    for table in tables:
                        if table:
                            # Build markdown table structure
                            md_table = "\n| " + " | ".join([str(cell or "") for cell in table[0]]) + " |\n"
                            md_table += "| " + " | ".join(["---"] * len(table[0])) + " |\n"
                            for row in table[1:]:
                                md_table += "| " + " | ".join([str(cell or "") for cell in row]) + " |\n"
                            markdown_output.append(md_table)
                    
                    # 3. Add text content
                    if text:
                        markdown_output.append(text)

            final_md = "\n\n".join(markdown_output)
            
            st.markdown(final_md)
            st.download_button("Download .md", final_md, "document.md")
            
        finally:
            os.remove(tmp_path)
