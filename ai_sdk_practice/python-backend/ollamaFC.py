from typing import Any, Callable, List, Optional, TypedDict, Union

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langgraph.graph import END, StateGraph
from langchain_google_vertexai.llms import VertexAI
from langchain_google_vertexai import ChatVertexAI
from langchain_community.chat_models import ChatOllama
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.tools import tool
from typing import Annotated, List, Tuple, Union
import functools
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field



llm = OllamaFunctions(model="llama3", format="json")
options = ["FINISH", "Search", "BIMDocumentInformationRetriever"]

# model = model.bind_tools(
#     tools=[
#         {
#             "name": "route",
#             "description": "Select the next role.",
#             "parameters": {
#                 "title": "routeSchema",
#                 "type": "object",
#                 "properties": {
#                     "next": {
#                         "title": "Next",
#                         "anyOf": [
#                             {"enum": options},
#                         ],
#                     },
#                 },
#                 "required": ["next"],
#             },
#         }
#     ],
#     function_call={"name": "route"},
# )

# @tool
# def router(
#     query: Annotated[str, "query to ask the retrieve information tool"]
#     ):
#   """Use Retrieval Augmented Generation to retrieve information about Building Information Modeling."""
#   return chain.invoke({"question":query})

model = llm.bind_tools(
    tools=[
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, " "e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["location"],
            },
        }
    ],
    function_call={"name": "get_current_weather"},
)

from langchain_core.messages import HumanMessage

print(model.invoke("what is the weather in Boston?"))


# system_prompt = """You are a supervisor tasked with managing a conversation between the"
#     following workers: Search, DocInformationRetriever. Given the following user request,"
#     respond with the tool to call next. Each tool will perform a"
#     task and respond with their results and status. When finished,"
#     respond with FINISH"""

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         MessagesPlaceholder(variable_name="messages"),
#         (
#             "system",
#             "Given the conversation above, answer the user questions",
#         ),
#     ]
# ).partial()


# chain = prompt | model | JsonOutputFunctionsParser()


# from langchain_core.messages import HumanMessage

# ans = chain.invoke({"messages": [HumanMessage(content="What is BIM")],})

# print(ans)

# def create_agent(
#     llm: OllamaFunctions,
#     tools: list,
#     system_prompt: str,
# ) -> str:
#     """Create a function-calling agent and add it to the graph."""
#     system_prompt += "\nWIork autonomously according to your specialty, using the tools available to you."
#     " Do not ask for clarification."
#     " Your other team members (and other teams) will collaborate with you with their own specialties."
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 system_prompt,
#             ),
#             MessagesPlaceholder(variable_name="messages"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )
#     agent = create_openai_functions_agent(llm, tools, prompt)
#     executor = AgentExecutor(agent=agent, tools=tools)
#     return executor

# class RouterResponse(BaseModel):
#     nextTool: str = Field(description="tool to be called next")

# parser = JsonOutputParser(pydantic_object=RouterResponse)

# prompt = PromptTemplate(
#     template="""You are an excellent router. You have the task to identify which tool to call to give justice to the users query.
#   you have two tools: DocumentRetrieverTool which answers questions based on Business Information Modelling and an estimation tool which give estimates to complete a job.\n{format_instructions}\n{query}\n""",
#     input_variables=["query"],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )




# @tool
# def retrieve_information(
#     query: Annotated[str, "query to ask the retrieve information tool"]
#     ):
#   """Use Retrieval Augmented Generation to retrieve information about Building Information Modeling."""
#   print("query",query)
#   return chain.invoke({"query":query})

# @tool
# def router(
#     query: Annotated[str, "query asked by the user"]
#     ):
#   """You are an excellent router. You have the task to identify which tool to call to give justice to the users query. And just give the name of the tool to call.
#   you have two tools: DocumentRetrieverTool which answers questions based on Business Information Modelling and an estimation tool which give estimates to complete a job"""
#   print("query",query)
#   router_chain = prompt | llm | parser

#   return chain.invoke({"query": query})


# research_agent = create_agent(
#     llm,
#     [retrieve_information],
#     "You are a research assistant who can provide specific information on the provided Building Information Modelling Document",
# )

# router_agent = create_agent(
#     llm,
#     [router],
#     "You are an excellent router. You have the task to identify which tool to call to give justice to the users query. you have two tools: DocumentRetrieverTool which answers questions based on Business Information Modelling and an estimation tool which give estimates to complete a job",
# )



# # print(router_agent.invoke({"messages": [HumanMessage(content="helo?")]}))

# # print(router.invoke({"query": [HumanMessage(content="helo?")]}))

# # print(router.invoke({"query":"What is BIM"}))

# r_chain = prompt | llm | parser
# print(r_chain.invoke({"query":"What is BIM"}))
