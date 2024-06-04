from langchain_community.embeddings import HuggingFaceEmbeddings,OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain.chains import  ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
import os
from langchain_pinecone import Pinecone
from langchain.memory import ConversationBufferMemory


llm_name = "gpt-3.5-turbo"

loader = PyPDFLoader("data/programming-language-pragmatics-2ed.pdf")
documents = loader.load()
text_splitter =  RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()    

db = Pinecone.from_texts(
    [t.page_content for t in docs],
    embedding=embeddings,
    index_name = "langchain-index"
)

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=False)

    
qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name=llm_name, temperature=0), 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=True,
    return_generated_question=True,
    memory=memory
    
)
    
chat_history = []
result = qa({"question": "What is abstraction", "chat_history": chat_history})
print(result["answer"]) 