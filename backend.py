import re
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
GEMINI_API_KEY="AIzaSyDmT3bsCKY7XLZLEhW59sHRgfkEVE0SxpQ"

def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()
    return data

def llm_pipeline(data):
    # API_KEY = st.secrets["GEMINI_API_KEY"]
    API_KEY=GEMINI_API_KEY
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=API_KEY,
        convert_system_message_to_human=True
    )
    chain = load_qa_chain(llm, chain_type="stuff")

    raw_output = chain.run(
        input_documents=data,
        question="""
        Generate exactly 10 important questions and their answers from the given content.
        (give the answer ,it must contain 5-7 lines ,highlight the answers that makes the people easy to study)
        Format:
        **Q1:** <question>
        **A1:** <answer>
        **Q2:** ...
        """
    )

    # Extract Q&A
    qa_pairs = re.findall(r"\*\*Q\d+:\*\*\s*(.*?)\s*\*\*A\d+:\*\*\s*(.*?)(?=\*\*Q\d+:\*\*|\Z)", raw_output, re.DOTALL)
    formatted_output = ""
    for i, (q, a) in enumerate(qa_pairs, 1):
        formatted_output += f"Question {i}: {q.strip()}\n\nAnswer: {a.strip()}\n\n{'-'*60}\n"
    
    if not qa_pairs:
        return "⚠️ No Q&A pairs detected. The model may have returned unexpected output."

    return formatted_output


