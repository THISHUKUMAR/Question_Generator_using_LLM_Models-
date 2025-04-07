import streamlit as st
import os
from backend import file_processing, llm_pipeline
from fpdf import FPDF

def export_to_pdf(text, filename="generated_qa.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        if line.strip() == "":
            pdf.ln()
        else:
            pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

st.set_page_config(page_title="PDF Q&A Generator", layout="centered")
st.title("📄 PDF to Q&A Generator")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Generate Q&A"):
        st.info("Generating questions and answers...")
        data = file_processing(file_path)
        result_text = llm_pipeline(data)
        st.success("Generation complete!")

        st.text_area("Generated Q&A", result_text, height=300)

        pdf_file_path = export_to_pdf(result_text)
        with open(pdf_file_path, "rb") as f:
            st.download_button("Download as PDF", f, file_name="generated_qa.pdf", mime="application/pdf")
