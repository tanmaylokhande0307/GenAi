from typing import Annotated,Any, List,TypedDict, Sequence
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import END, StateGraph
import operator
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolInvocation
import json
from langchain_core.messages import FunctionMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from chain import ragTool,session_id,store
from estimator import is_valid_estimator_input
from router import question_router, router_model, tool_executor
from summarizer import summary_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


graph_agent_sys_prompt = """You are an expert tool calling assistant {messages}"""
graph_agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", graph_agent_sys_prompt),
        ("human", "{messages}"),
    ]
)


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        messages: generated messages from the LLM
    """

    messages: Annotated[Sequence[BaseMessage], operator.add]
    question: str
    

def route_question(state):
    """
    Route question to rag tool or estimator tool.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    question = state["question"]
    tool = question_router.invoke({"question": question})
    if tool.toolName == "rag_tool":
        print("---ROUTE QUESTION TO rag_tool---")
        return "rag"  
    elif tool.toolName == "estimator_tool":
        print("---ROUTE QUESTION TO estimator_tool---")
        return "estimate"


def  call_agent(state):
    """
    Get estimates

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): updated state
    """

    question = state["question"]
    print(question)

    model_chain = graph_agent_prompt | router_model
    response = model_chain.invoke(question)
    return {"messages": [response], "question": question}

        
def check_estimator_inputs(state):
    messages = state["messages"]
    last_message = messages[-1]
    args = last_message.tool_calls[0]["args"]
    is_valid, message = is_valid_estimator_input(args)
    if is_valid:
        print("The object has been successfully created as EstimatorInput.")
        return "valid"
    else:
       return "not_valid"

def call_estimator_tool(state):
    messages = state["messages"]
    last_message = messages[-1]
    args = last_message.tool_calls[0]["args"]
        
    action = ToolInvocation(
        tool=last_message.tool_calls[0]["name"],
        tool_input=args,
    )
    response = tool_executor.invoke(action)
    msg_parts = []

    # Check and add each part based on the presence of the keys
    if "Name" in args:
        msg_parts.append(f"named {args['Name']}")
    if "Category" in args:
        msg_parts.append(f"of category {args['Category']}")
    if "NewCount" in args:
        msg_parts.append(f"with new count as {args['NewCount']}")
    if "SaveAsCount" in args:
        msg_parts.append(f"saveas count as {args['SaveAsCount']}")
    if "CloneCount" in args:
        msg_parts.append(f"and clone count as {args['CloneCount']}")

    # Join the parts with a space
    job_drawing_info = ' '.join(msg_parts)

    # Initialize parts of the estimation message
    estimation_parts = []

    # Check and add each part based on the presence of the keys
    if "TotalNewhrs" in response:
        estimation_parts.append(f"TotalNewhrs: {response['TotalNewhrs']}")
    if "TotalSaveAshrs" in response:
        estimation_parts.append(f"TotalSaveAshrs: {response['TotalSaveAshrs']}")
    if "TotalClonehrs" in response:
        estimation_parts.append(f"TotalClonehrs: {response['TotalClonehrs']}")

    # Join the parts with a comma and space
    estimation_info = ', '.join(estimation_parts)

    # Combine the two parts into the final message
    msg_string = f"Estimation for a Job or Drawing {job_drawing_info} came out to be as follows: {estimation_info}"
    summary = summary_chain.invoke(msg_string)
    message_to_be_stored_in_session = AIMessage(content=summary)
    store[session_id].messages.append(message_to_be_stored_in_session)
    function_message = FunctionMessage(content=str(response), name=action.tool,summary=summary)
    return {"messages": [function_message]}

def call_rag_tool(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updated state
    """
    print("---GENERATE---")
    question = state["question"]
    
    response = ragTool.invoke({"question": question.content})
    response_message = AIMessage(content=str(response), name="RagTool")

    return {"messages": [response_message]}

memory = SqliteSaver.from_conn_string(":memory:")


graph = StateGraph(GraphState)

graph.add_node("rag_tool", call_rag_tool)
graph.add_node("agent", call_agent)
graph.add_node("estimator_tool",call_estimator_tool)
# graph.add_node("generate_answer",generate_answer)

graph.set_conditional_entry_point(route_question, {
    "rag": "rag_tool",
    "estimate": "agent"
})

graph.add_conditional_edges("agent",check_estimator_inputs, {
    "valid": "estimator_tool",
    "not_valid": "rag_tool"
})

graph.add_edge("rag_tool", END)
graph.add_edge("estimator_tool", END)
# graph.add_edge("generate_answer",END)

chain = graph.compile(checkpointer=memory)

inputs = {
        "question": HumanMessage(content="Give me the estimation for job named External Wall Sandwich Panel with category TeklaModelling new count as 44, saveas count as 44 and clone count as 59")
    }

answer = chain.invoke(inputs,{"configurable":{"thread_id":"7"}})["messages"]
print("answer",answer)
# print(memory)