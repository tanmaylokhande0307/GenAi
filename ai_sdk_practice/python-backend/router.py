from langchain_experimental.llms.ollama_functions import OllamaFunctions

from langchain.pydantic_v1 import BaseModel, Field
from typing import Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.prebuilt import ToolExecutor
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.utils.function_calling import convert_pydantic_to_openai_function
from langchain.agents import create_openai_functions_agent


from typing import Annotated,Any, List, Optional,TypedDict, Sequence
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
import numpy as np
import pandas as pd
from langchain_core.pydantic_v1 import BaseModel, Field
from estimator import estimatorTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


ROUTER_LLM = OllamaFunctions(model="llama3", format="json")

router_system_prompt = """You are an expert at routing a user question to a rag_tool or estimator_tool.
The estimator_tool is used when the user wants to know the time required or estimate to complete a given job provided all the arguments like job name, category, new count. Otherwise, use rag_tool."""

router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", router_system_prompt),
        ("human", "{question}"),
    ]
)


class RouteQuery(BaseModel):
    """Route a user query to the most relevant tool."""

    toolName: Literal["rag_tool", "estimator_tool"] = Field(
        ...,
        description="Given a user question choose to route it to rag_tool or estimator_tool.",
    )
    
class Response(BaseModel):
    """Final answer to the user"""

    result: str = Field(description="the result of the retrieval or estimation")
    explanation: str = Field(
        description="explanation of the steps taken to get the result"
    )
    

structured_llm_router = ROUTER_LLM.with_structured_output(RouteQuery)

question_router = router_prompt | structured_llm_router

tools = [estimatorTool]

tool_executor = ToolExecutor(tools)

# Bind tools to the model
functions = [format_tool_to_openai_function(t) for t in tools]
# Bind the resposne to the model
functions.append(convert_pydantic_to_openai_function(Response))

router_model = ROUTER_LLM.bind_tools(functions)

from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# agent_runnable = create_openai_functions_agent(ROUTER_LLM, tools, prompt)


# print(
#     tool_executor.invoke({input:"How much time will it take me to complete TeklaModelling of Precast Wall"})
# )
# print(question_router.invoke({"question": "What is BIM?"}))

# res = router_model.invoke( [HumanMessage(content="Give me the estimation for job named External Wall Sandwich Panel with category TeklaModelling new count as 44, saveas count as 44 and clone count as 59")])
# from langgraph.prebuilt import ToolInvocation
# action = ToolInvocation(
#     tool=res.tool_calls[0]["name"],
#     tool_input=res.tool_calls[0]["args"],
# )
# response = tool_executor.invoke(action)
# print(response)
