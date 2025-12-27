import argparse
import gradio as gr
from openai import OpenAI

# Argument parser setup
parser = argparse.ArgumentParser(
    description="Chatbot Interface with Customizable Parameters"
)
parser.add_argument(
    "--model-url", type=str, default="http://localhost:12000/v1", help="Model URL"
)
parser.add_argument(
    "-m", "--model", type=str, help="Model name for the chatbot",default="Qwen3-14B"
)
parser.add_argument(
    "--temp", type=float, default=0.8, help="Temperature for text generation"
)
parser.add_argument(
    "--stop-token-ids", type=str, default="", help="Comma-separated stop token IDs"
)
parser.add_argument("--host", type=str, default="0.0.0.0")
parser.add_argument("--port", type=int, default=12004)

# Parse the arguments
args = parser.parse_args()

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "empty"
openai_api_base = args.model_url

# Create an OpenAI client to interact with the API server
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def predict(message, history):
    # Convert chat history to OpenAI format
    history_openai_format = [
        {"role": "system", "content": "You are a great ai assistant."}
    ]
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    # Create a chat completion request and send it to the API server
    stream = client.chat.completions.create(
        model=args.model,  # Model name to use
        messages=history_openai_format,  # Chat history
        temperature=args.temp,  # Temperature for text generation
        stream=True,  # Stream response
        extra_body={
            "repetition_penalty": 1,
            "stop_token_ids": (
                [int(id.strip()) for id in args.stop_token_ids.split(",") if id.strip()]
                if args.stop_token_ids
                else []
            ),
        },
    )

    # Read and return generated text from response stream
    partial_message = ""
    in_think = False

    for chunk in stream:
        delta = chunk.choices[0].delta

        if not delta or not delta.content:
            continue

        text = delta.content

        # Handle <think> block
        if "<think>" in text:
            in_think = True
            continue

        if "</think>" in text:
            in_think = False
            continue

        if in_think:
            continue

        partial_message += text
        yield partial_message

    # 对于qwen3-14b这种prompt中带<think>会失败
    # for chunk in stream:
    #     partial_message += chunk.choices[0].delta.content or ""
    #     yield partial_message

# Create and launch a chat interface with Gradio
gr.ChatInterface(predict).queue().launch(
    server_name=args.host, server_port=args.port, share=False
)