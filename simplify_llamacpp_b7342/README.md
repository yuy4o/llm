## Basic Use

`Dockerfile` is used to build the minimum llama.cpp server image.

`llama-server` command related params: https://github.com/ggml-org/llama.cpp/tree/b7342/tools/server

```shell
docker build -t llama.cpp:server-b7342 .

# 先创建容器，进入容器拉起服务
docker run -d -p 5001:5001 -v /workspaces/yuy4o:/app llama.cpp:server-b7342 tail -f /dev/null
llama-server -m /app/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf --port 5006 --host 0.0.0.0

# 创建容器同时拉起服务
docker run -d \
  --name llama-server \
  -p 5006:5006 \
  -v /data1/jiangyy/2llamacpp-b7342/2llamacpp-b7342/llama.cpp:/app \
  llamacppserver:v2 \
  llama-server \
  -m /app/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf \
  --host 0.0.0.0 \
  --port 5006

# 容器外查看模型日志 
docker logs -f llama-server
```

```shell
curl -X POST http://localhost:5006/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf",
        "messages": [
          {
            "role": "system",
            "content": "你是一个有帮助的 AI 助手。"
          },
          {
            "role": "user",
            "content": "帮我生成一个随机数，直接返回我数字"
          }
        ],
        "max_tokens": 512,
        "temperature": 0,
        "top-p": 0.9,
        "repeat-penalty": 1.1,
        "stream": false
      }'

```

## Function Calling

use `--jinja -fa on --chat-template-file /app/Qwen3-Coder.jinja` to open function calling: https://github.com/ggml-org/llama.cpp/blob/b7342/docs/function-calling.md

`Qwen3-Coder.jinja` is the template for the interface function calling: https://github.com/ggml-org/llama.cpp/blob/b7342/models/templates/Qwen3-Coder.jinja

```shell
docker run -d \
  --name llama-server \
  -p 5006:5006 \
  -v /data1/jiangyy/2llamacpp-b7342/2llamacpp-b7342/llama.cpp:/app \
  llamacppserver:v2 \
  llama-server \
  --jinja \
  -fa on \
  -m /app/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf \
  --chat-template-file /app/Qwen3-Coder.jinja \
  --host 0.0.0.0 \
  --port 5006
```

大模型工具调用是在用户两次（或多次）请求大模型中间，加上自定义函数处理，将处理结果作为第二次大模型的输入得到最终答案。这个过程有点像 rag，函数处理结果类似检索出的知识库内容，作为额外信息提交给模型

还会在提示词中加入[工具调用的提示词](https://huggingface.co/deepseek-ai/DeepSeek-V3.1#toolcall)，帮助模型被请求后**自发**地确定是否调用工具或检索知识库

第一次调用：
```shell
curl http://localhost:5006/v1/chat/completions -d '{
    "model": "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf",
    "messages": [
        {"role": "system", "content": "You are a chatbot that uses tools/functions. Dont overthink things."},
        {"role": "user", "content": "What is the weather in Istanbul?"}
    ],
    "tools": [{
        "type":"function",
        "function":{
            "name":"get_current_weather",
            "description":"Get the current weather in a given location",
            "parameters":{
                "type":"object",
                "properties":{
                    "location":{
                        "type":"string",
                        "description":"The city and country/state, e.g. `San Francisco, CA`, or `Paris, France`"
                    }
                },
                "required":["location"]
            }
        }
    }]
}'

# {"choices":[{"finish_reason":"tool_calls","index":0,"message":{"role":"assistant","content":null,"tool_calls":[{"type":"function","function":{"name":"get_current_weather","arguments":"{\"location\":\"Istanbul\"}"},"id":"iPsUCwl1rBHV3C2nxJdqIlju7oLGJSX6"}]}}],"created":1765875493,"model":"Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf","system_fingerprint":"b0-unknown","object":"chat.completion","usage":{"completion_tokens":24,"prompt_tokens":309,"total_tokens":333},"id":"chatcmpl-AXxYMparoHy2RK67FTYzT7JRJZCa2qXn","timings":{"cache_n":308,"prompt_n":1,"prompt_ms":57.488,"prompt_per_token_ms":57.488,"prompt_per_second":17.39493459504592,"predicted_n":24,"predicted_ms":1079.521,"predicted_per_token_ms":44.980041666666665,"predicted_per_second":22.232082562543944}}
```

传入工具执行结果第二次调用：
```shell
curl http://localhost:5006/v1/chat/completions -d '{
  "model": "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf",
  "messages": [
    {"role":"user","content":"What is the weather in Istanbul?"},
    {
      "role":"assistant",
      "tool_calls":[
        {
          "id":"iPsUCwl1rBHV3C2nxJdqIlju7oLGJSX6",
          "type":"function",
          "function":{
            "name":"get_current_weather",
            "arguments":"{\"location\":\"Istanbul\"}"
          }
        }
      ]
    },
    {
      "role":"tool",
      "tool_call_id":"iPsUCwl1rBHV3C2nxJdqIlju7oLGJSX6",
      "content":"{\"temperature\":\"18°C\",\"condition\":\"Partly cloudy\"}"
    }
  ]
}'


# {"choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"The current weather in Istanbul is 18°C with partly cloudy conditions."}}],"created":1765875707,"model":"Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf","system_fingerprint":"b0-unknown","object":"chat.completion","usage":{"completion_tokens":16,"prompt_tokens":65,"total_tokens":81},"id":"chatcmpl-TzYjHTUauZ0hKmOJX6haDYmCF5fVwmvK","timings":{"cache_n":64,"prompt_n":1,"prompt_ms":49.496,"prompt_per_token_ms":49.496,"prompt_per_second":20.203652820429934,"predicted_n":16,"predicted_ms":615.282,"predicted_per_token_ms":38.455125,"predicted_per_second":26.004336223065195}}
```

完整流程见 [tool_call.py](tool_call.py)