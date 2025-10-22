import os
import agentscope
from agentscope.agents import DialogAgent
from agentscope.agents import UserAgent

def main() -> None:
    """A basic conversation demo"""

    dashscope_example_config = {
      "model_type": "dashscope_chat",
      "config_name": "tongyi_qwen_config",
      "model_name": "qwen-plus-2025-01-25",
      "api_key": f"{os.environ.get('DASHSCOPE_API_KEY')}",
    }
    agentscope.init(
        model_configs=[dashscope_example_config],
    )

    dialog_agent = DialogAgent(
        name="Assistant",
        sys_prompt="You're a helpful assistant.",
        model_config_name="tongyi_qwen_config",
    )
    user_agent = UserAgent()

    x = None
    while x is None or x.content != "exit":
        x = dialog_agent(x) 
        x = user_agent(x)
        
# INSTALLATION:
# git clone https://github.com/modelscope/agentscope.git
# cd agentscope
# pip install -e .[full]

# RUNNING:
# as_gradio agentui.py