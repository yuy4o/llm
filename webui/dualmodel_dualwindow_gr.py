# 页面分左右两个窗口，针对两个模型同时问答
import argparse
import gradio as gr
from openai import OpenAI
import asyncio

parser = argparse.ArgumentParser(description="Chatbot Interface with Model Switching")
parser.add_argument(
    "--models", nargs='+', action='append',
    metavar=('NAME', 'URL'), help="Model name and its corresponding URL"
)
parser.add_argument(
    "--temp", type=float, default=0.8, help="Temperature for text generation"
)
parser.add_argument(
    "--stop-token-ids", type=str, default="", help="Comma-separated stop token IDs"
)
parser.add_argument("--host", type=str, default="0.0.0.0")
parser.add_argument("--port", type=int, default=12005)

args = parser.parse_args()

if args.models:
    models = {model[0]: model[1] for model in args.models}
else:
    models = {
        "Qwen3-14B": "http://localhost:12000/v1",
        "Qwen3-4B": "http://localhost:12002/v1"
    }

current_model_name_1 = list(models.keys())[0]
current_model_name_2 = list(models.keys())[1]
display_model_name = list(models.keys())[0]
current_model_url_1 = models[current_model_name_1]
current_model_url_2 = models[current_model_name_2]

openai_api_key = "empty"

client_1 = OpenAI(
    api_key=openai_api_key,
    base_url=current_model_url_1,
)

client_2 = OpenAI(
    api_key=openai_api_key,
    base_url=current_model_url_2,
)

def switch_model_1(model_name):
    global current_model_name_1, current_model_url_1, client_1
    if model_name is not None and model_name in models:
        current_model_name_1 = model_name
        current_model_url_1 = models[model_name]
        client_1 = OpenAI(
            api_key=openai_api_key,
            base_url=current_model_url_1,
        )

def switch_model_2(model_name):
    global current_model_name_2, current_model_url_2, client_2
    if model_name is not None and model_name in models:
        current_model_name_2 = model_name
        current_model_url_2 = models[model_name]
        client_2 = OpenAI(
            api_key=openai_api_key,
            base_url=current_model_url_2,
        )

async def predict_1(message, history, model_name):
    switch_model_1(model_name)
    
    history_openai_format = [
        {"role": "system", "content": "You are a great ai assistant."}
    ]
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    stream = client_1.chat.completions.create(
        model=current_model_name_1, 
        messages=history_openai_format,
        temperature=args.temp, 
        stream=True, 
        extra_body={
            "repetition_penalty": 1,
            # "stop_token_ids": (
            #     [int(id.strip()) for id in args.stop_token_ids.split(",") if id.strip()]
            #     if args.stop_token_ids
            #     else []
            # ),
        },
    )

    partial_message = ""
    async def sync_to_async_iter(sync_iter):
        for item in sync_iter:
            await asyncio.sleep(0)  # Yield control to event loop without blocking
            yield item

    in_think = False
    async for chunk in sync_to_async_iter(stream):
        delta = chunk.choices[0].delta

        # if delta.content:
        #     partial_message += delta.content
        #     yield partial_message
        if not delta or not delta.content:
            continue

        text = delta.content

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

    # async for chunk in sync_to_async_iter(stream):
    #     partial_message += chunk.choices[0].delta.content or ""
    #     yield partial_message  # Yield each part of the message as it comes

async def predict_2(message, history, model_name):
    switch_model_2(model_name)
    
    history_openai_format = [
        {"role": "system", "content": "You are a great ai assistant."}
    ]
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    stream = client_2.chat.completions.create(
        model=current_model_name_2, 
        messages=history_openai_format,
        temperature=args.temp, 
        stream=True, 
        extra_body={
            "repetition_penalty": 1,
            # "stop_token_ids": (
            #     [int(id.strip()) for id in args.stop_token_ids.split(",") if id.strip()]
            #     if args.stop_token_ids
            #     else []
            # ),
        },
    )

    partial_message = ""
    async def sync_to_async_iter(sync_iter):
        for item in sync_iter:
            await asyncio.sleep(0)  # Yield control to event loop without blocking
            yield item

    in_think = False
    async for chunk in sync_to_async_iter(stream):
        delta = chunk.choices[0].delta

        # if delta.content:
        #     partial_message += delta.content
        #     yield partial_message
        if not delta or not delta.content:
            continue

        text = delta.content

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

    # async for chunk in sync_to_async_iter(stream):
    #     partial_message += chunk.choices[0].delta.content or ""
    #     yield partial_message  # Yield each part of the message as it comes


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            model_dropdown_1 = gr.Dropdown(choices=list(models.keys()), value=display_model_name, label="Select Model 1")
            chat_history_1 = gr.Textbox(lines=40, label="Chat History", interactive=False)
            user_input_1 = gr.Textbox(lines=1, label="Your Message")
            send_button_1 = gr.Button("Send")
            
            history_1 = []

            async def update_chat_1(message, model_name):
                global history_1
                response = ""
                async for chunk in predict_1(message, history_1, model_name):
                    response = chunk
                history_1.append((message, response))
                chat_history_1.value = "\n".join([f"User: {m}\nAI: {r}" for m, r in history_1])
                return chat_history_1.value

            send_button_1.click(fn=update_chat_1, inputs=[user_input_1, model_dropdown_1], outputs=chat_history_1)

        with gr.Column():
            model_dropdown_2 = gr.Dropdown(choices=list(models.keys()), value=display_model_name, label="Select Model 2")
            chat_history_2 = gr.Textbox(lines=40, label="Chat History", interactive=False)
            user_input_2 = gr.Textbox(lines=1, label="Your Message")
            send_button_2 = gr.Button("Send")
            
            history_2 = []

            async def update_chat_2(message, model_name):
                global history_2
                response = ""
                async for chunk in predict_2(message, history_2, model_name):
                    response = chunk
                history_2.append((message, response))
                chat_history_2.value = "\n".join([f"User: {m}\nAI: {r}" for m, r in history_2])
                return chat_history_2.value

            send_button_2.click(fn=update_chat_2, inputs=[user_input_2, model_dropdown_2], outputs=chat_history_2)

demo.launch(server_name=args.host, server_port=args.port, share=False)