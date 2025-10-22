from agentscope.agents import DialogAgent, UserAgent
import agentscope
import dashscope
dashscope.api_key = f"{os.environ.get('DASHSCOPE_API_KEY')}"

# # 无效
# agentscope.init(
#     model_configs=[
#         {
#             "config_name": "my_config",
#             "model_type": "dashscope_chat",
#             "api_url": "http://172.27.221.3:12000/v1/chat/completions",
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Authorization": "Authorization: Bearer empty"
#             },
#             "json_args": {
#                 "model": "/data1/jiangyy/Qwen3-14B",
#             }
#         }
#     ]
# )

# 配置
agentscope.init(
    model_configs={
        "config_name": "my_config",
        "model_name": "qwen-plus-2025-01-25",
        "model_type": "dashscope_chat",
    },
)

# # 双agent对话
# angel = DialogAgent(
#     name="Angel",
#     sys_prompt="你是一个名叫 Angel 的歌手，说话风格简单凝练。",
#     model_config_name="my_config",
# )

# monster = DialogAgent(
#     name="Monster",
#     sys_prompt="你是一个名叫 Monster 的运动员，说话风格简单凝练。",
#     model_config_name="my_config",
# )

# msg = None
# for _ in range(5):
#     msg = angel(msg)
#     msg = monster(msg)


# 多agent报数
from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg
from agentscope import msghub
import agentscope
import time

alice = DialogAgent(
    name="Alice",
    sys_prompt="你是一个名叫Alice的助手。",
    model_config_name="my_config",
)

bob = DialogAgent(
    name="Bob",
    sys_prompt="你是一个名叫Bob的助手。",
    model_config_name="my_config",
)

charlie = DialogAgent(
    name="Charlie",
    sys_prompt="你是一个名叫Charlie的助手。",
    model_config_name="my_config",
)

# 介绍对话规则
greeting = Msg(
    name="user",
    content="现在开始从1开始逐个报数，每次只产生一个数字，绝对不能产生其他任何信息。",
    role="user",
)

with msghub(
    participants=[alice, bob, charlie],
    announcement=greeting,  # 开始时，通知消息将广播给所有参与者。
) as hub:
    # 对话的第一轮
    alice()
    bob()
    bob()
    time.sleep(5)

    # 对话的第2轮
    alice()
    charlie()
    charlie()
    time.sleep(5)

    # 对话的第3轮
    alice()
    bob()
    charlie()
    time.sleep(5)



# # 创建一个对话智能体和一个用户智能体
# dialog_agent = DialogAgent(
#     name="Friday",
#     model_config_name="my_config",
#     sys_prompt="你是一个名为Friday的助手"
# )

# user_agent = UserAgent(name="user")

# # # 显式构建工作流程/对话
# x = None
# while x is None or x.content != "exit":
#     x = dialog_agent(x)
#     x = user_agent(x)