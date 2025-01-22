# https://github.com/openai/swarm

from swarm import Swarm, Agent
from openai import OpenAI

client = OpenAI(api_key="empty", base_url="http://localhost:8777/v1")##

client = Swarm(client=client)

def instructions(context_variables):
    name = context_variables.get("name", "User")
    return f"You are a helpful agent. Greet the user by name ({name})."

def print_account_details(context_variables: dict):
    user_id = context_variables.get("user_id", None)
    name = context_variables.get("name", None)
    print(f"Account Details: {name} {user_id}")
    return "Success"

agent = Agent(
    name="Agent",
    instructions=instructions,
    functions=[print_account_details],
    model="/data/wenhr/modelhub/Qwen2.5-Coder-32B-Instruct",##
    tool_choice="none",##
)

context_variables = {"name": "James", "user_id": 123}

response = client.run(
    messages=[{"role": "user", "content": "Hi!"}],
    agent=agent,
    context_variables=context_variables,
)
print(response.messages[-1]["content"])

response = client.run(
    messages=[{"role": "user", "content": "Print my account details!"}],
    agent=agent,
    context_variables=context_variables,
    stream=True,
)

# print(response.messages[-1]["content"])

chunks = list(response)[1:-2]
for chunk in chunks:
    print(chunk['content'], end='', flush=False)