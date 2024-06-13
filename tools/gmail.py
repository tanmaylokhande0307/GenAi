from dotenv import load_dotenv

load_dotenv()

from langchain.agents.agent_toolkits import GmailToolkit

from langchain import OpenAI
from langchain.agents import initialize_agent, AgentType

from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)



from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

llm = ChatOpenAI(temperature=0)

agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    # This is set to False to prevent information about my email showing up on the screen
    # Normally, it is helpful to have it set to True however.
    verbose=False,
)

agent_executor.invoke(
    {
        "input": "Create a gmail draft for me to edit of a letter from the perspective of a sentient parrot"
        " who is looking to collaborate on some research with her"
        " estranged friend, a cat. Under no circumstances may you send the message, however."
    }
)


