import transformers

tokenizer = transformers.AutoTokenizer.from_pretrained("DeepSeek-V3.1-Base")


tools = [
    {
        "name": "bash",
        "description": "Run commands in a bash shell",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to run"}
            },
            "required": ["command"]
        }
    }
]

def build_deepseek_tool_prompt(tools: list):
    """
    将 tools 转成 DeepSeek V3 格式的 tool_description 字符串
    """
    txt = "## Tools\nYou have access to the following tools:\n\n"
    for tool in tools:
        name = tool["name"]
        desc = tool["description"]
        params = tool["parameters"]

        txt += f"### {name}\n"
        txt += f"Description: {desc}\n\n"
        txt += f"Parameters: {params}\n\n"

    return txt


messages = [
    {"role": "system", "content": "You are a helpful assistant" + build_deepseek_tool_prompt(tools)},
    {"role": "user", "content": "Who are you?"},
    {"role": "assistant", "content": "<think>Hmm</think>I am DeepSeek"},
    {"role": "user", "content": "1+1=?"}
]

# print(tokenizer.apply_chat_template(messages, tokenize=False, thinking=True, add_generation_prompt=True))
# '<｜begin▁of▁sentence｜>You are a helpful assistant<｜User｜>Who are you?<｜Assistant｜></think>I am DeepSeek<｜end▁of▁sentence｜><｜User｜>1+1=?<｜Assistant｜><think>'

print(tokenizer.apply_chat_template(messages, tokenize=False, thinking=False, add_generation_prompt=True))
# <｜begin▁of▁sentence｜>You are a helpful assistant## Tools
# You have access to the following tools:

# ### bash
# Description: Run commands in a bash shell

# Parameters: {'type': 'object', 'properties': {'command': {'type': 'string', 'description': 'The bash command to run'}}, 'required': ['command']}

# <｜User｜>Who are you?<｜Assistant｜></think>I am DeepSeek<｜end▁of▁sentence｜><｜User｜>1+1=?<｜Assistant｜></think>


# https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Base
# <｜begin▁of▁sentence｜>{system prompt}\n\n{tool_description}<｜User｜>{query}<｜Assistant｜></think> where the tool_description is

# ## Tools
# You have access to the following tools:

# ### {tool_name1}
# Description: {description}

# Parameters: {json.dumps(parameters)}

# IMPORTANT: ALWAYS adhere to this exact format for tool use:
# <｜tool▁calls▁begin｜><｜tool▁call▁begin｜>tool_call_name<｜tool▁sep｜>tool_call_arguments<｜tool▁call▁end｜>{additional_tool_calls}<｜tool▁calls▁end｜>

# Where:
# - `tool_call_name` must be an exact match to one of the available tools
# - `tool_call_arguments` must be valid JSON that strictly follows the tool's Parameters Schema
# - For multiple tool calls, chain them directly without separators or spaces