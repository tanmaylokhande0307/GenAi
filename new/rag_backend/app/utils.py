from langchain_community.chat_models import ChatOllama


llm = ChatOllama(model="llama3", temperature=0)

print(llm.invoke("Explain GenAi in long paragraph")) 
