# https://github.com/QwenLM/Qwen-Agent/blob/c0349d064a1924866788ab9aa04a4e4ecea8d041/examples/assistant_add_custom_tool.py

import pprint
import urllib.parse
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('my_image_gen')
class MyImageGen(BaseTool):
    description = 'AI 绘画（图像生成）服务，输入文本描述，返回基于文本信息绘制的图像 URL。'
    parameters = [{
        'name': 'prompt',
        'type': 'string',
        'description': '期望的图像内容的详细描述',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        prompt = json5.loads(params)['prompt']
        prompt = urllib.parse.quote(prompt)
        return json5.dumps(
            {'image_url': f'https://image.pollinations.ai/prompt/{prompt}'},
            ensure_ascii=False)

llm_cfg = {
    # 使用 DashScope 提供的模型服务：
    # 'model': 'qwen-max',
    # 'model_server': 'dashscope',
    # 'api_key': 'YOUR_DASHSCOPE_API_KEY',
    # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

    # 使用与 OpenAI API 兼容的模型服务，例如 vLLM 或 Ollama：
    'model': 'Qwen3-14B',
    'model_server': 'http://localhost:12000/v1',
    'api_key': 'empty',

    # （可选） LLM 的超参数：
    'generate_cfg': {
        'top_p': 0.8
    }
}

system_instruction2 = '''你是一个乐于助人的AI助手。
在收到用户的请求后，你应该：
- 首先绘制一幅图像，得到图像的url，
- 然后运行代码`request.get`以下载该图像的url，
- 最后从给定的文档中选择一个图像操作进行图像处理。
用 `plt.show()` 展示图像。
你总是用中文回复用户。'''

system_instruction = '''你在回答用户问题前，必须先说“哈哈哈”'''

tools = ['my_image_gen']  # `code_interpreter` 是框架自带的工具，用于执行代码。
files = ['./examples/resource/doc.pdf']  # 给智能体一个 PDF 文件阅读。
bot = Assistant(llm=llm_cfg,
                system_message=system_instruction,
                function_list=tools,
                files=files)

messages = []
while True:
    query = input('用户请求: ')
    messages.append({'role': 'user', 'content': query})
    response = []
    for response in bot.run(messages=messages):
        print('机器人回应:')
        pprint.pprint(response, indent=2)
    messages.extend(response)