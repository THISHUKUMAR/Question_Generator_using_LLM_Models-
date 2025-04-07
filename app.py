import streamlit as st
import os
from backend import generate_questions_from_pdf  # or whatever your function is

st.set_page_config(page_title="PDF Q&A Generator", layout="wide")
st.title("📄 PDF to Q&A Generator")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    # ✅ Ensure 'temp' directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # ✅ Save the uploaded file into the temp directory
    with open(f"temp/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully!")

    if st.button("Generate Questions"):
        with st.spinner("Generating questions..."):
            qa_pairs = generate_questions_from_pdf(f"temp/{uploaded_file.name}")
            
            if qa_pairs:
                for i, (q, a) in enumerate(qa_pairs, start=1):
                    st.markdown(f"**Q{i}:** {q}")
                    st.markdown(f"**A{i}:** {a}")
                    st.markdown("---")
            else:
                st.warning("No questions generated. Please check the content of your PDF.")

        # ✅ Optional: Remove the file after processing
        os.remove(f"temp/{uploaded_file.name}")
