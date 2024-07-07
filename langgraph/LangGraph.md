**LangGraph** builds on top  of LangChain and makes it very easy to build [[Agents]]
Langraph makes it easy to customize agent runtime

##### Graph State
graph state will be passed throughout  the life cycle of the graph
each node can push updates in the state so we dont have to pass the entire state from node to node everytime
We need to specify what type of update to push in the state
By default existing state is overriden

#### Define the graph state
1. `input`: This is the input string representing the main ask from the user, passed in as input.
2. `chat_history`: This is any previous conversation messages, also passed in as input.
3. `intermediate_steps`: This is list of actions and corresponding observations that the agent takes over time. This is updated each iteration of the agent.
4. `agent_outcome`: This is the response from the agent, either an AgentAction or AgentFinish. The AgentExecutor should finish when this is an AgentFinish, otherwise it should call the requested tools.

```python
class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction,str]], operator.add]
```
#### Define the nodes and the edges
We now need to define a few different nodes in our graph. In `langgraph`, a node can be either a function or a [runnable](https://python.langchain.com/v0.2/docs/concepts/#langchain-expression-language-lcel). There are two main nodes we need for this:

1. _The agent_: responsible for deciding what (if any) actions to take.
2. _A function to invoke tools_: if the agent decides to take an action, this node will then execute that action.

We will also need to define some edges. 

1. _Conditional Edge_:
2. _Normal Edge_: after the tools are invoked, it should always go back to the agent to decide what to do next

#### Define Graph
```python
from langgraph.graph import END, StateGraph, START

workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()
```
