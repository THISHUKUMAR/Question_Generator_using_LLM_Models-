def file_processing(file_path):
    # File loading and processing
    from langchain.document_loaders import PyPDFLoader
    file = file_path
    loader = PyPDFLoader(file)
    data = loader.load()
    return data


import re
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI

def llm_pipeline(data):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")

    # Prompt to generate Q&A
    raw_output = chain.run(
        input_documents=data,
        question="Generate 10 important questions and their answers."
    )

    # Extract questions and answers using regex
    qa_pairs = re.findall(
        r"\*\*\d+\.\s*Question:\*\*\s*(.*?)\s*\*\*Answer:\*\*\s*(.*?)(?=(\*\*\d+\.|\Z))",
        raw_output,
        re.DOTALL
    )

    # Format neatly
    formatted_output = ""
    for i, (question, answer, _) in enumerate(qa_pairs, 1):
        formatted_output += f"Question {i}:\n{question.strip()}\n\nAnswer:\n{answer.strip()}\n"
        formatted_output += "-" * 50 + "\n"

    return formatted_output
