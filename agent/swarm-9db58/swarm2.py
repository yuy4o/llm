# https://github.com/openai/swarm/tree/9db581cecaacea0d46a933d6453c312b034dbf47

from swarm import Swarm, Agent
from openai import OpenAI

client = OpenAI(api_key="empty", base_url="http://localhost:12000/v1")

client = Swarm(client=client)

def instructions(context_variables):
    name = context_variables.get("name", "User")
    return f"You are a helpful agent. Greet the user by name ({name})."

def print_account_details(context_variables: dict):
    user_id = context_variables.get("user_id", None)
    name = context_variables.get("name", None)
    print(f"Account Details: {name} {user_id}")
    return "Success"

def func(context_variables):
    if "cat" in context_variables.get("user_id", None):
        return "my dog's name is meow"
    else:
        return "woof"

agent = Agent(
    name="Agent",
    instructions=instructions,
    functions=[print_account_details, func],
    model="Qwen3-14B",
    tool_choice="none",
)

context_variables = {"name": "James", "user_id": "cat", }

# non-stream calling
response = client.run(
    messages=[{"role": "user", "content": "Hi!call the tool named func to get what is my dog's name"}],
    agent=agent,
    context_variables=context_variables,
    stream=False,
)
print(response.messages[-1]["content"])


# stream calling
response = client.run(
    messages=[{"role": "user", "content": "Hi!call the tool named func to get what is my dog's name"}],
    agent=agent,
    context_variables=context_variables,
    stream=True,
)
chunks = list(response)[1:-2]
for chunk in chunks:
    print(chunk['content'], end='', flush=False)
