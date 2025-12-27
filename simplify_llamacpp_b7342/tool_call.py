import json
import requests

LLAMA_URL = "http://localhost:5006/v1/chat/completions"
MODEL = "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf"


def get_current_weather(location: str) -> dict:
    return {
        "location": location,
        "temperature": "20°C",
        "condition": "Partly cloudy"
    }

def run_weather_chat():
    # ========== 第 1 步：让模型决定是否调用工具 ==========
    first_payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a chatbot that uses tools/functions. Dont overthink things."
            },
            {
                "role": "user",
                "content": "What is the weather in Istanbul?"
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ],
        "tool_choice": "auto"
    }

    r1 = requests.post(LLAMA_URL, json=first_payload)
    r1.raise_for_status()
    resp1 = r1.json()

    choice = resp1["choices"][0]
    message = choice["message"]

    if "tool_calls" not in message:
        raise RuntimeError("Model did not request a tool call")

    tool_call = message["tool_calls"][0]
    tool_id = tool_call["id"]
    args = json.loads(tool_call["function"]["arguments"])

    # ========== 第 2 步：执行工具 ==========
    weather_result = get_current_weather(args["location"])

    # ========== 第 3 步：把 tool 结果喂回模型 ==========
    second_payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "What is the weather in Istanbul?"
            },
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_id,
                        "type": "function",
                        "function": {
                            "name": "get_current_weather",
                            "arguments": json.dumps(args)
                        }
                    }
                ]
            },
            {
                "role": "tool",
                "tool_call_id": tool_id,
                "content": json.dumps(weather_result)
            }
        ]
    }

    r2 = requests.post(LLAMA_URL, json=second_payload)
    r2.raise_for_status()
    resp2 = r2.json()

    # ========== 最终结果 ==========
    final_message = resp2["choices"][0]["message"]["content"]
    return final_message


if __name__ == "__main__":
    answer = run_weather_chat()
    print("Final answer:\n", answer)

# Final answer:
#  The current weather in Istanbul is 20°C with partly cloudy conditions.