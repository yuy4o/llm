# https://github.com/openai/swarm/tree/9db581cecaacea0d46a933d6453c312b034dbf47

# 触发的是 Swarm 的 Agent Handoff 机制，建议使用 deepseek api

from swarm import Swarm, Agent
from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

client = Swarm(client=client)

def transfer_to_agent_b():
    return agent_b

agent_a = Agent(
    name="Agent A",
    model="deepseek-chat",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    model="deepseek-chat",
    instructions="Only speak in Haikus.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
)

print(response.messages[-1]["content"])
