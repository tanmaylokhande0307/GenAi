from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from dotenv import load_dotenv
import vertexai
from langchain_google_vertexai import VertexAI


load_dotenv()

vertexai.init(project="gemini-api-428204", location="us-central1")
model = VertexAI(model_name="gemini-pro")

analysis_system_template_str = """Give a detailed analysis of the user's input based on the below context .Analyze the context and the user's input and generate an analysis which will include the user's input and information like hours per job for specific job. 
Don't mention the word 'context' anywhere in the response just state the hours per job from the context and provide the analysis as per the input along with time required to do one job from the context. Also give total hours estimation.
If the context doesn't contain any relevant information to the input, don't make something up and give a generalized analysis of the input.
...{context}
"""

analysis_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=analysis_system_template_str
    )
)

analysis_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"], template="{question}"
    )
)

messages = [analysis_system_prompt, analysis_human_prompt]
analysis_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)


def get_splitter(chunk_size , chunk_overlap , separators,length_function,is_separator_regex= False,):
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=length_function,
        is_separator_regex=is_separator_regex
    )

def read_csvs_from_folder(folder_path): 
    docs = []
    for filename in os.listdir(folder_path):
        csv_path = os.path.join(folder_path, filename)
        if filename.lower().endswith('.csv'):
            doc = CSVLoader(file_path=csv_path).load()
            docs = docs + doc    
    return docs

def chunk_data(document):
    text_splitter = get_splitter(chunk_size=1000, chunk_overlap=50, separators=["\n", " "], length_function=len,is_separator_regex=False)
    chunks = text_splitter.transform_documents(document)
    return chunks

def provision_vector_store(documents,persist_dir, embeddings):
    Chroma.from_documents(documents=documents, embedding=embeddings,persist_directory=persist_dir)
    
def provision_retriever(persist_dir, embeddings):
    return Chroma(persist_directory=persist_dir, embedding_function=embeddings).as_retriever()
    


csv_docs = read_csvs_from_folder("data")
csv_chunks = chunk_data(csv_docs)

provision_vector_store(documents=csv_chunks,embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),persist_dir="AGENT_VECTOR_STORE_DIR")

analysis_retriever = provision_retriever(persist_dir="AGENT_VECTOR_STORE_DIR",embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))


# docs = retriever.invoke("Estimation for a Job or Drawing External Wall Sandwich Panel came out to be as follows: 'TotalNewhrs': 283.8, 'TotalSaveAshrs': 141.9, 'TotalClonehrs': 95.1375")
                                                            

summary_chain = (
    {"context": analysis_retriever, "question": RunnablePassthrough()}
    | analysis_prompt_template
    | model
    | StrOutputParser()
)


# ans = summary_chain.invoke("Estimation for a Job or Drawing External Wall Sandwich Panel came out to be as follows: 'TotalNewhrs': 283.8, 'TotalSaveAshrs': 141.9, 'TotalClonehrs': 95.1375")
# print(ans)