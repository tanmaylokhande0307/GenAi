from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from streaming import streamingFunc
import asyncio
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage

load_dotenv()

embedding_function = OpenAIEmbeddings()

chat = ChatOpenAI(callbacks=[StreamingStdOutCallbackHandler()], streaming=True)

# print(chat([HumanMessage(content="what is the weather in sf. write 200 words")]))
for ch in chat([HumanMessage(content="what is the weather in sf. write 200 words")]):
    print(ch)

# docs = [
#     Document(
#         page_content="the dog loves to eat pizza", metadata={"source": "animal.txt"}
#     ),
#     Document(
#         page_content="the cat loves to eat lasagna", metadata={"source": "animal.txt"}
#     ),
# ]

# db = Chroma.from_documents(docs, embedding_function)
# retriever = db.as_retriever()


# template = """Answer the question based only on the following context:
# {context}

# Question: {question}
# """
# prompt = ChatPromptTemplate.from_template(template)
# model = ChatOpenAI(temperature=0, streaming=True)

# retrieval_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | model
#     | StrOutputParser()
# )

app = FastAPI()

# async def generate_chat_responses(message):
#     async for chunk in retrieval_chain.astream(message):
#         content = chunk.replace("\n", "<br>")
#         yield f"data: {content}\n\n"


# @app.get("/")
# async def root():
#     return FileResponse("static/index.html")


# @app.get("/chat_stream/{message}")
# async def chat_stream(message: str):
#     return chat([HumanMessage(content=message)])


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)