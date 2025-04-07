def file_processing(file_path):
    from langchain.document_loaders import PyPDFLoader
    from langchain.schema import Document
    import streamlit as st

    try:
        loader = PyPDFLoader(file_path)
        data = loader.load()

        # Debug: Show loaded data
        st.write("✅ Loaded documents from PDF:", data)

        # If no content, fallback to sample doc
        if not data or len(data) == 0:
            st.warning("⚠️ No content found in PDF. Using sample data.")
            data = [Document(page_content="The solar system includes the Sun and celestial objects like planets, moons, and asteroids.")]
        return data

    except Exception as e:
        st.error(f"❌ Failed to process PDF: {e}")
        return [Document(page_content="Sample fallback document content.")]


import re
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document

def llm_pipeline(data):
    # Load API key from Streamlit secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]

    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY)

    # Load question answering chain
    chain = load_qa_chain(llm, chain_type="stuff")

    try:
        # Debug: Show first part of loaded document content
        st.write("First document content preview:", data[0].page_content[:300] if data else "No content")

        # Generate Q&A
        raw_output = chain.run(
            input_documents=data,
            question="Generate 10 important questions and their answers."
        )
    except Exception as e:
        st.error(f"❌ Error during LLM processing: {e}")
        return ""

    # Extract Q&A with regex
    qa_pairs = re.findall(
        r"\*\*\d+\.\s*Question:\*\*\s*(.*?)\s*\*\*Answer:\*\*\s*(.*?)(?=(\*\*\d+\.|\Z))",
        raw_output,
        re.DOTALL
    )

    # Format results
    formatted_output = ""
    for i, (question, answer, _) in enumerate(qa_pairs, 1):
        formatted_output += f"Question {i}:\n{question.strip()}\n\nAnswer:\n{answer.strip()}\n"
        formatted_output += "-" * 50 + "\n"

    return formatted_output
