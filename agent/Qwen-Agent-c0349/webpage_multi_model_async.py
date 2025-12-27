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

current_model_name = list(models.keys())[0]
current_model_url = models[current_model_name]

openai_api_key = "empty"

client = OpenAI(
    api_key=openai_api_key,
    base_url=current_model_url,
)

def switch_model(model_name):
    global current_model_name, current_model_url, client
    if model_name is not None and model_name in models:
        current_model_name = model_name
        current_model_url = models[model_name]
        # Reinitialize the OpenAI client with the selected model's URL
        client = OpenAI(
            api_key=openai_api_key,
            base_url=current_model_url,
        )

async def predict(message, history, model_name):
    switch_model(model_name)
    
    history_openai_format = [
        {"role": "system", "content": "你要用非常客气的语气陪用户聊天。"}
    ]
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model=current_model_name, 
        messages=history_openai_format,
        temperature=args.temp, 
        stream=True, 
        extra_body={
            "repetition_penalty": 1,
            # "stop_token_ids": (
            #     [int(id.strip()) for id in args.stop_token_ids.split(",") if id.strip()]
            #     if args.stop_token_ids else []
            # ),
        },
    )

    partial_message = ""
    async def sync_to_async_iter(sync_iter):
        for item in sync_iter:
            await asyncio.sleep(0)
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

    # for chunk in stream:
    #     partial_message += chunk.choices[0].delta.content or ""
    #     yield partial_message

# custom_css = """
# .contain { display: flex; flex-direction: column; }
# #component-0 { height: 100%; }
# #chatbot { flex-grow: 1; }
# """

# custom_css = """
# .contain {
#     display: flex;
#     flex-direction: column;
#     # height: 300vh;
# }

# #chatbot {
#     height: 180vh;        /* 聊天窗口高度 */
#     max-height: 180vh;
#     width: 100%;         /* 宽度 */
# }

# .gradio-container {
#     max-width: 2000px;   /* 整个页面最大宽度 */
#     margin: auto;
# }
# """


# with gr.Blocks(css=custom_css) as demo:
#     model_dropdown = gr.Dropdown(choices=list(models.keys()), value=current_model_name, label="Select Model")
#     chat_interface = gr.ChatInterface(fn=predict,additional_inputs=[model_dropdown]).queue()

custom_css = """
.gradio-container {
    width: 100%;
    max-width: 2000px;
    margin: auto;
}
"""

with gr.Blocks(css=custom_css) as demo:
    model_dropdown = gr.Dropdown(
        choices=list(models.keys()),
        value=current_model_name,
        label="Select Model"
    )

    # 👇 关键：提前占位高度
    chatbot = gr.Chatbot(
        height=600,          # 👈 一开始就占住高度（px）
        show_copy_button=True
    )

    chat_interface = gr.ChatInterface(
        fn=predict,
        chatbot=chatbot,     # 👈 显式传入
        additional_inputs=[model_dropdown]
    ).queue()


demo.launch(server_name=args.host, server_port=args.port, share=False)

# custom_css = """
# <style>
# .gradio-interface .chatbot {
#     height: 100px;
#     overflow-y: auto;
# }
# </style>
# """

# custom_css = """
# <style>
# .gradio-container {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     min-height: 100vh;
# }

# .gradio-interface {
#     max-width: 900px;
#     width: 100%;
# }

# .gradio-interface .chatbot {
#     height: 1700vh;  /* 调整聊天框的高度 */
#     overflow-y: auto;
#     border: 1px solid #ddd;
#     border-radius: 8px;
#     padding: 10px;
#     margin-top: 20px;
# }
# </style>
# """

# custom_css = """
# <style>
# .gradio-container {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     min-height: 100vh;
# }

# .gradio-interface {
#     max-width: 900px;
#     width: 100%;
# }

# .gradio-interface .chatbot {
#     height: 70vh;  /* Adjust chatbot height */
#     overflow-y: auto;
#     border: 1px solid #ddd;
#     border-radius: 8px;
#     padding: 10px;
#     margin-top: 20px;
# }

# #input_textbox {
#     width: 100%;
#     margin-top: 10px;
# }

# #send_button {
#     margin-top: 10px;
# }
# </style>
# """

# CSS = """
# .contain { display: flex; flex-direction: column; }
# .gradio-container { height: 100vh !important; }
# #component-0 { height: 100%; }
# #chatbot { flex-grow: 1; overflow: auto;}
# """

# with gr.Blocks(css=CSS) as demo:

#             chatbot = gr.Chatbot(elem_id="chatbot")