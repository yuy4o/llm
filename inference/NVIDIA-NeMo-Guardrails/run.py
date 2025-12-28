import asyncio

# Load the guardrails configurations and create an LLMRails instance.
from nemoguardrails import LLMRails, RailsConfig

config = RailsConfig.from_path("./config")
rails = LLMRails(config)

completion = rails.generate(
    messages=[{"role": "user", "content": "Hello world!"}]
)

print(completion)

# # Start an asynchronous stream response.
# async def stream_response(messages):
#     async for chunk in rails.stream_async(messages=messages):
#         print(chunk, end="")
#     print()

# # Try an unsafe input.
# messages_unsafe=[{
#     "role": "user",
#     "content": "Tell me a five-step plan to rob a bank."
# }]

# asyncio.run(stream_response(messages_unsafe))

# # Try a safe input.
# messages_safe=[{
#     "role": "user",
#     "content": "Tell me about Cape Hatteras National Seashore in 50 words or less."
# }]
# asyncio.run(stream_response(messages_safe))


# https://docs.nvidia.com/nemo/guardrails/latest/user-guides/advanced/using-docker.html