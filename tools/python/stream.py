# openai async client - streaming response
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main():
    stream = await client.chat.completions.create(
        model = "gpt-4",
        messages = [{
            "role":"user",
            "content":"Say this is a test."
        }
        ],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
    
asyncio.run(main())