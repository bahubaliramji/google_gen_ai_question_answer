# from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()


import time

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ['GOOGLE_API_KEY'], temperature=.7)

# from langchain_community.document_loaders.csv_loader import CSVLoader



embeddings = HuggingFaceEmbeddings()
vector_db_file_path="faiss_index"

def create_vector_db():
    print("in create_vector_db")

    loader = CSVLoader('codebasics_faqs.csv', source_column='prompt')
    docs = loader.load()
    vectordb = FAISS.from_documents(documents=docs, embedding=embeddings)

    vectordb.save_local(vector_db_file_path)   
    print("in create_vector_db done")





def get_qa_chain():
    print("in get_qa_chain")
    vectordb = FAISS.load_local(vector_db_file_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt":PROMPT}
    )
    print("in get_qa_chain done")

    return chain



if __name__ == "__main__":
    
    # create_vector_db()
    chain = get_qa_chain()

    print(chain("do you provide internship?"))


print("hello done")

