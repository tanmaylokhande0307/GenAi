from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores.utils import filter_complex_metadata
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]


text_splitter = RecursiveCharacterTextSplitter( 
    chunk_size = 700,
    chunk_overlap = 50
)

docs = PyPDFLoader(file_path="../attention.pdf").load()
chunks = text_splitter.split_documents(docs)
chunks = filter_complex_metadata(chunks)
embeddings = FastEmbedEmbeddings()
vector_store = FAISS.from_documents(docs, embeddings)
retriever = vector_store.as_retriever()
llm = ChatOllama(model="llama3", temperature=0)
template = """Answer the question based only on the following context. If you cannot answer the question with the context, please respond with 'I don't know':

Context:
{context}

Question:
{question}
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prompt = ChatPromptTemplate.from_template(template)

retrieval_augmented_qa_chain = (
    {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
    | RunnablePassthrough.assign(context=itemgetter("context"))
    | {"response": prompt | llm, "context": itemgetter("context")}
)

question = "What are the major changes in v0.1.0?"

result = retrieval_augmented_qa_chain.invoke({"question" : question})


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, retrieval_augmented_qa_chain, path="/response")

prompt1 = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt1 | llm,
    path="/joke",
)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
