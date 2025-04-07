import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"
import streamlit as st
from backend import file_processing, llm_pipeline
from io import BytesIO

st.set_page_config(page_title="📄 PDF to Q&A Generator")

st.title("📄 PDF to Q&A Generator")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with st.spinner("Reading PDF..."):
        with open(f"temp/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        data = file_processing(f"temp/{uploaded_file.name}")
        st.success("PDF successfully processed!")

    with st.spinner("Generating questions and answers..."):
        result_text = llm_pipeline(data)
        st.success("Q&A generation complete!")
        st.text_area("Generated Q&A", result_text, height=400)

        # Option to download Q&A
        def create_download():
            buffer = BytesIO()
            buffer.write(result_text.encode())
            buffer.seek(0)
            return buffer

        st.download_button("Download Q&A", create_download(), file_name="QA_output.txt")
