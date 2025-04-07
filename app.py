import streamlit as st
import os
from backend import file_processing, llm_pipeline

# Set page configuration
st.set_page_config(page_title="PDF Q&A Generator", layout="centered")

# App title
st.title("📄 PDF Question Generator using Gemini")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Create temp directory if it doesn't exist
if uploaded_file:
    os.makedirs("temp", exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join("temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the file and generate questions
    with st.spinner("Processing and generating questions..."):
        try:
            data = file_processing(file_path)
            output = llm_pipeline(data)
            st.success("✅ Done!")

            # Display results
            st.markdown("### 📌 Generated Questions and Answers")
            st.text_area("Output", output, height=400)

            # Download button
            st.download_button(
                label="📥 Download Q&A as TXT",
                data=output,
                file_name="generated_questions.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
