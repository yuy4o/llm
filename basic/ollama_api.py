import requests

# 定义要发送的数据
data = {
    "model": "gemma:2b", # https://ollama.com/download/OllamaSetup.exe 下载好客户端后运行 `ollama run gemma:2b`下载模型
    "messages": [
        {
            "role": "system",
            "content": "你是个帮助用户解答问题的好帮手"
        },
        {
            "role": "user",
            "content": "周树人和鲁迅什么关系"
        }
    ],
    "stream": False
}


# 发送POST请求
response = requests.post("http://localhost:11434/api/chat", json=data)

# 检查响应
if response.status_code == 200:
    print("请求成功！")
    print("响应内容：", response.text)
    print("响应答案：", response.json()['message']['content'])
else:
    print("请求失败！状态码：", response.status_code)