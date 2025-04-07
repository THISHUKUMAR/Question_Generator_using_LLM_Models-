import streamlit as st
import google.generativeai as genai
import pdfplumber
import re
from fpdf import FPDF

# -----------------------
# Streamlit Page Config
# -----------------------
st.set_page_config(page_title="📄 PDF to Q&A Generator")
st.title("📄 PDF to Q&A Generator")
st.write("Upload a PDF and get 10 questions and answers from its content!")

# -----------------------
# Google Gemini API Key
# -----------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------
# Extract text from PDF
# -----------------------
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])

# -----------------------
# Generate Q&A from text using Gemini
# -----------------------
def generate_qa_with_gemini(text):
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
Read the following content and generate 10 questions and answers based on it.

Format:
Q1: <question>
A1: <answer>
...
Q10: <question>
A10: <answer>

Text:
{text}
"""

    response = model.generate_content(prompt)
    raw_output = response.text

    # Extract Q&A using regex
    qa_pairs = re.findall(r"Q\d+:\s*(.*?)\s*A\d+:\s*(.*?)(?=\s*Q\d+:|\Z)", raw_output, re.DOTALL)

    if not qa_pairs:
        return "❌ Failed to extract Q&A. Raw output:\n" + raw_output

    formatted_output = ""
    for i, (q, a) in enumerate(qa_pairs, 1):
        formatted_output += f"**Question {i}:**\n{q.strip()}\n\n**Answer:**\n{a.strip()}\n\n---\n"

    return formatted_output.strip()

# -----------------------
# Convert Q&A text to downloadable PDF
# -----------------------
def create_pdf_from_text(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf

# -----------------------
# File Upload
# -----------------------
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    st.success("✅ PDF uploaded!")

    with st.spinner("Extracting text and generating Q&A..."):
        text = extract_text_from_pdf(uploaded_file)
        result = generate_qa_with_gemini(text)

    st.markdown("### 📋 Generated Q&A")
    st.markdown(result)

    # Clean text for PDF
    if result and "Question" in result:
        result_text = re.sub(r"\*\*|\n\n---\n", "", result)
        pdf = create_pdf_from_text(result_text)
        pdf_bytes = bytes(pdf.output(dest="S").encode("latin1"))

        st.download_button(
            label="📥 Download Q&A as PDF",
            data=pdf_bytes,
            file_name="QA_output.pdf",
            mime="application/pdf"
        )
