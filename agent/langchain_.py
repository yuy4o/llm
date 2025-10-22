from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

llm = ChatOpenAI(
    model="Qwen3-14B",
    api_key="empty",  # 你在 vllm serve 里设的 --api-key
    base_url="http://localhost:12000/v1"
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

# Run the agent
print(agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
))

# breakpoint()

# """
# 带工具的 LangGraph Agent 示例
# 这个示例展示了如何创建一个能够使用工具的 Agent。
# Agent 可以根据用户请求选择合适的工具来完成任务。
# """
# from typing import Annotated, Literal
# from typing_extensions import TypedDict
# import os
# import requests
# from datetime import datetime
# import json
# from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# from langchain_core.tools import tool
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode, create_react_agent

# # 加载环境变量
# load_dotenv()

# # 定义状态结构
# class State(TypedDict):
#     """Agent 状态定义"""
#     messages: Annotated[list, add_messages]

# # 定义工具
# @tool
# def get_weather(city: str) -> str:
#     """
#     获取指定城市的天气信息

#     Args:
#         city: 城市名称

#     Returns:
#         str: 天气信息
#     """
#     # 这里使用模拟数据，实际应用中可以调用真实的天气API
#     weather_data = {
#         "北京": "晴天, 温度 15-25° C, 微风",
#         "上海": "多云, 温度 18-28° C, 东南风",
#         "广州": "小雨, 温度 20-30° C, 南风",
#         "深圳": "阴天, 温度 22-32° C, 无风",
#         "杭州": "晴天, 温度 16-26° C, 西北风",
#     }
#     return weather_data.get(city, f"抱歉, 暂时无法获取 {city} 的天气信息")


# @tool
# def calculate(expression: str) -> str:
#     """
#     计算数学表达式

#     Args:
#         expression: 数学表达式，如 "2+3*4"

#     Returns:
#         str: 计算结果
#     """
#     try:
#         # 仅允许基本的整数运算
#         allowed_chars = set("0123456789+-*/.()")
#         if not all(c in allowed_chars for c in expression):
#             return "错误: 表达式包含不被允许的字符"

#         result = eval(expression)
#         return f"{expression} = [result]"
#     except Exception as e:
#         return f"计算错误: {str(e)}"


# @tool
# def get_current_time() -> str:
#     """
#     获取当前时间

#     Returns:
#         str: 当前时间
#     """
#     now = datetime.now()
#     return now.strftime("%Y年%m月%d日 %H:%M:%S")


# @tool
# def search_wikipedia(query: str) -> str:
#     """
#     搜索维基百科

#     Args:
#         query: 搜索关键词

#     Returns:
#         str: 搜索结果摘要
#     """
#     try:
#         # 使用维基百科API搜索
#         search_url = f"https://zh.wikipedia.org/api/rest_v1/page/summary/{query}"
#         response = requests.get(search_url, timeout=5)

#         if response.status_code == 200:
#             data = response.json()
#             return f"标题: [data.get('title', '未知')]\\n摘要: [data.get('extract', '无摘要信息')]"
#         else:
#             return f"搜索失败, 无法找到关于 '{query}' 的信息"
#     except Exception as e:
#         return f"搜索出错: [str(e)]"



