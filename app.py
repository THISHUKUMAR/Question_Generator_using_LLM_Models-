# import streamlit as st
# import os
# from backend import file_processing, llm_pipeline

# # Set page configuration
# st.set_page_config(page_title="PDF Q&A Generator", layout="centered")

# # App title
# st.title("📄 Important Question Generator ")

# # File uploader
# uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# # Create temp directory if it doesn't exist
# if uploaded_file:
#     os.makedirs("temp", exist_ok=True)

#     # Save the uploaded file
#     file_path = os.path.join("temp", uploaded_file.name)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Process the file and generate questions
#     with st.spinner("Processing and generating questions..."):
#         try:
#             data = file_processing(file_path)
#             output = llm_pipeline(data)
#             st.success("✅ Done!")

#             # Display results
#             st.markdown("### 📌 Generated Questions and Answers")
#             st.text_area("Output", output, height=400)

#             # Download button
#             st.download_button(
#                 label="📥 Download Q&A as TXT",
#                 data=output,
#                 file_name="generated_questions.txt",
#                 mime="text/plain"
#             )

#         except Exception as e:
#             st.error(f"❌ An error occurred: {e}")

import streamlit as st
from backend import generate_questions_from_pdf
from fpdf import FPDF
import os

st.set_page_config(page_title="PDF Q&A Generator", layout="centered")

st.title("📄 PDF Question Generator with Gemini ✨")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Processing... ⏳"):
        # Save uploaded PDF temporarily
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        try:
            result = generate_questions_from_pdf(temp_path)
            st.success("✅ Questions and answers generated!")
            st.markdown("### 🔍 Extracted Q&A:")
            st.text(result)

            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            for line in result.split("\n"):
                pdf.multi_cell(0, 10, txt=line)

            pdf_output_path = f"temp/{uploaded_file.name}_QA.pdf"
            pdf.output(pdf_output_path)

            # Read and offer download
            with open(pdf_output_path, "rb") as f:
                st.download_button(
                    label="📥 Download Q&A as PDF",
                    data=f,
                    file_name="QnA_Output.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

