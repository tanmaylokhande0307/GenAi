from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain.chains import  ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
import os

llm_name = "gpt-3.5-turbo"


loader = PyPDFLoader("data/123.pdf")
documents = loader.load()
text_splitter =  RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings()

url = "http://localhost:6333"
collection_name = "gpt_db"

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    path="/tmp/local_qdrant",
    collection_name="my_documents",
)


retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    
qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name=llm_name, temperature=0), 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=True,
    return_generated_question=True,
)
    

result = qa({"question": "What is BIM", "chat_history": []})
print(result["answer"])