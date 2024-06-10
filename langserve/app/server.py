from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain.vectorstores import FAISS
import os
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI 
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

hf_llm = ChatOpenAI(model="gpt-3.5-turbo")

embeddings_model = OpenAIEmbeddings()

faiss_index = FAISS.load_local("langserve_index", embeddings_model,allow_dangerous_deserialization=True)
retriever = faiss_index.as_retriever()

prompt_template = """\
Use the provided context to answer the user's question. If you don't know the answer, say you don't know.

Context:
{context}

Question:
{question}"""

rag_prompt = ChatPromptTemplate.from_template(prompt_template)

entry_point_chain = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
rag_chain = entry_point_chain | rag_prompt | hf_llm | StrOutputParser()


# Edit this to add the chain you want to add
add_routes(app, rag_chain,path="/rag")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
