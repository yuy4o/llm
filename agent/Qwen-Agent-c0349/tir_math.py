# https://github.com/QwenLM/Qwen-Agent/blob/c0349d064a1924866788ab9aa04a4e4ecea8d041/examples/tir_math.py

"""A TIR(tool-integrated reasoning) math agent
```bash
python tir_math.py
```
"""
import os
from pprint import pprint

from qwen_agent.agents import TIRMathAgent
from qwen_agent.gui import WebUI

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')

# We use the following two systems to distinguish between COT mode and TIR mode
TIR_SYSTEM = """Please integrate natural language reasoning with programs to solve the problem above, and put your final answer within \\boxed{}."""
COT_SYSTEM = """Please reason step by step, and put your final answer within \\boxed{}."""


def init_agent_service():
    # Use this to access the qwen2.5-math model deployed on dashscope
    # llm_cfg = {'model': 'qwen2.5-math-72b-instruct', 'model_type': 'qwen_dashscope', 'generate_cfg': {'top_k': 1}}
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
    bot = TIRMathAgent(llm=llm_cfg, name='Qwen3-14B', system_message=TIR_SYSTEM)
    return bot


def test(query: str = '调用python_executor执行 """x=3;y=5;x+y"""'):
    bot = init_agent_service()
    messages = [{'role': 'user', 'content': query}]
    for response in bot.run(messages):
        pprint(response, indent=2)


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        # Query example: 斐波那契数列前10个数字
        query = input('user question: ')
        messages.append({'role': 'user', 'content': query})
        response = []
        for response in bot.run(messages):
            print('bot response:', response)
        messages.extend(response)


def app_gui():
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            r'曲线 $y=2 \\ln (x+1)$ 在点 $(0,0)$ 处的切线方程为 $( )$.',
            'A digital display shows the current date as an $8$-digit integer consisting of a $4$-digit year, '
            'followed by a $2$-digit month, followed by a $2$-digit date within the month. '
            'For example, Arbor Day this year is displayed as 20230428. '
            'For how many dates in $2023$ will each digit appear an even number of times '
            'in the 8-digital display for that date?'
        ]
    }
    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
    test()
    # app_tui()
    # app_gui()
