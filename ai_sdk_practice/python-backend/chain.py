from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_google_vertexai import VertexAI
from dotenv import load_dotenv
load_dotenv()
# from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import asyncio


model = VertexAI(model_name="gemini-pro")



# model = ChatOllama(model="llama3")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

prompt = PromptTemplate.from_template(
            """
            <s> [INST] Answer the users question based on the retrieved context. If you do not find an answer in the context, respond with i dont know[/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

docs = PyPDFLoader(file_path="data/BIM.pdf").load()
chunks = text_splitter.split_documents(docs)
chunks = filter_complex_metadata(chunks)
# vector_store = Chroma.from_documents(documents=chunks, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),persist_directory="db")
retriever = Chroma(persist_directory="db", embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001")).as_retriever()
# print(vector_store)

chain = ({"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser())

# print(chain.invoke("What is BIM"))


# async def read_events():
#         events = []
#         num_events = 0
#         async for event in chain.astream_events("hello", version="v1"):
#                 kind = event["event"]
#                 if kind == "on_parser_start":
#                         print(
#                                 f"Chat model chunk: {repr(event['data']['chunk'])}",
#                                 flush=True,
#                                 )
#                 if kind == "on_chain_stream":
#                     print(f"Parser chunk: {event['data']['chunk']}", flush=True)
#                 if kind == "on_llm_stream":
#                     print(f"Parser chunk: {event['data']['chunk']}", flush=True)      
#                 num_events += 1
#                 if num_events > 30:
#                     # Truncate the output
#                     print("...")
#                 break
#                 # print(event, flush=True)



#         # return events

# asyncio.run(read_events())

















