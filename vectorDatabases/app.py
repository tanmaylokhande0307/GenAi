import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() 
    return text        

def get_text_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks
    

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

def handle_input(user_question):
    docs = st.session_state.vector_store.similarity_search(query=user_question,k=3)
    llm = ChatOpenAI(temperature=0)
    chain = load_qa_chain(llm=llm,chain_type="stuff")
    response = chain.run(input_documents=docs,question=user_question)
    st.write(response)


def main():
    load_dotenv()
    
    st.set_page_config(page_title='Chat Bot')
        
    st.header("chatbot")
    user_question = st.text_input("Ask questions based on your pdf")
    if user_question:
        handle_input(user_question)
    
    
    with st.sidebar:
        st.subheader("pdf's")
        pdf_docs = st.file_uploader("Upload your pdf",accept_multiple_files=True)
        if st.button('Process'):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                
                text_chunks = get_text_chunks(raw_text)

                vector_store = get_vector_store(text_chunks)
                st.session_state.vector_store = vector_store    
                

if __name__ == '__main__':
    main()