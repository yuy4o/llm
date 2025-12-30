import gradio as gr
import requests
from openai import OpenAI

def ask_model_stream(user_input):
    client = OpenAI(
        base_url="http://localhost:12000/v1",
        api_key="empty",
    )

    model = client.models.list().data[0].id

    stream = client.chat.completions.create(
    model= model,
    messages=[
        # {"role": "system", "content": ""},
        {"role": "user", "content": user_input}
    ],
    temperature=0.7,
    max_tokens=4096,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=True
    )

    # response = completion.choices[0].message.content

    partial = ""

    # 👉 可选但强烈推荐：提前 yield 一次，占位 UI
    yield partial

    for chunk in stream:
        delta = chunk.choices[0].delta
        if not delta or not delta.content:
            continue

        partial += delta.content
        yield partial

    # if response.status_code != 200:
    #     yield f"Error: {response.status_code} - {response.text}"
    #     return

    # 流式处理返回结果
    # partial_response = ""
    # for chunk in response.iter_lines():
    #     if chunk:
    #         try:
    #             data = chunk.decode("utf-8").strip()
    #             if data.startswith("data:"):
    #                 data = data[len("data:"):].strip()
    #             if data == "[DONE]":
    #                 break
                
    #             # 解析 JSON 数据
    #             content = eval(data).get("choices", [{}])[0].get("delta", {}).get("content", "")
    #             if content:
    #                 partial_response += content
    #                 yield partial_response
    #         except Exception as e:
    #             yield f"Error parsing chunk: {str(e)}"
    #             return

# 使用 Gradio 构建界面
with gr.Blocks() as demo:
    gr.Markdown("# AI问答助手\n实时回答你的问题，支持流式输出。")
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="输入你的问题", placeholder="在这里输入...", lines=2)
            ask_button = gr.Button("发送问题")
        with gr.Column():
            chatbot = gr.Textbox(label="AI回答", lines=30, interactive=False)
    
    # 绑定事件
    ask_button.click(ask_model_stream, inputs=user_input, outputs=chatbot)

# 启动界面
demo.launch(server_name="0.0.0.0", server_port=12005, share=False)
