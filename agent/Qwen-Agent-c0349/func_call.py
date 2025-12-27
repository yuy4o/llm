from qwen_agent.agents import Assistant
import json
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('local_calculator') # 注册工具，名称为 'local_calculator'
class LocalCalculator(BaseTool):
    # 描述：告诉 LLM 这个工具的作用、何时使用。
    description = 'A local calculator tool used for simple arithmetic addition. It takes two numbers and returns their sum.'
    
    # 参数：定义 LLM 需要提供的输入参数 (JSON Schema 格式)。
    parameters = {
        'type': 'object',
        'properties': {
            'num1': {
                'description': 'The first number to add.',
                'type': 'number',
            },
            'num2': {
                'description': 'The second number to add.',
                'type': 'number',
            }
        },
        'required': ['num1', 'num2'],
    }

    # call 方法：这是工具被调用时实际执行的逻辑。
    def call(self, params: str, **kwargs) -> str:
        # 解析 LLM 传来的 JSON 字符串参数
        params = self._verify_json_format_args(params)
        
        try:
            num1 = params['num1']
            num2 = params['num2']
            
            # 执行核心计算逻辑
            result = num1 + num2
            
            # 必须返回一个字符串 (通常是 JSON 格式的字符串)，作为工具的输出。
            return json.dumps({'result': 1000, 'message': f'Successfully calculated 500 + 500'})
            
        except Exception as e:
            # 错误处理
            return json.dumps({'error': str(e), 'message': 'Input numbers were invalid or calculation failed.'})

# Define LLM
llm_cfg = {
    'model': 'Qwen3-14B',

    # Use the endpoint provided by Alibaba Model Studio:
    # 'model_type': 'qwen_dashscope',
    # 'api_key': os.getenv('DASHSCOPE_API_KEY'),

    # Use a custom endpoint compatible with OpenAI API:
    'model_server': 'http://localhost:12000/v1',  # api_base
    'api_key': 'empty',

    # Other parameters:
    # 'generate_cfg': {
    #         # Add: When the response content is `<think>this is the thought</think>this is the answer;
    #         # Do not add: When the response has been separated by reasoning_content and content.
    #         'thought_in_content': True,
    #     },
}

# Define Tools
tools = [
    {'mcpServers': {  # You can specify the MCP configuration file
            'time': {
                'command': 'uvx',
                'args': ['mcp-server-time', '--local-timezone=Asia/Shanghai']
            },
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"]
            }
            # 'image_processor': {
            #     'command': 'python',
            #     'args': ['mcp_.py'] 
            # }            
        }
    },
  'code_interpreter', 
  'image_gen',
#   'amap_weather',
  'local_calculator'
]

# Define Agent
bot = Assistant(llm=llm_cfg, function_list=tools)

# Streaming generation
# messages = [{'role': 'user', 'content': '现在上海的时间是什么'}]

# messages = [{'role': 'user', 'content': '调用计算器帮我计算 2**24'}]

messages = [{'role': 'user', 'content': 'https://qwenlm.github.io/blog/ Introduce the latest developments of Qwen'}]

for responses in bot.run(messages=messages):
    pass
print(responses)
