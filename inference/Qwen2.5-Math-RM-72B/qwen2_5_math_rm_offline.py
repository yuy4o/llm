import torch
from transformers import AutoModel, AutoTokenizer

model_name = "/data1/jiangyy/models/Qwen2.5-Math-RM-72B"
device = "auto"

model = AutoModel.from_pretrained(
    model_name, 
    device_map=device, 
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
).eval() # 切换模型到推理模式，确保推理结果稳定

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

chat = [
    {"role": "system", "content": "Please reason step by step, and put your final answer within \\boxed{}."},
    {"role": "user", "content": "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?"},
    {"role": "assistant", "content": "To determine how much Janet makes from selling the duck eggs at the farmers' market, we need to follow these steps:\n\n1. Calculate the total number of eggs laid by the ducks each day.\n2. Determine how many eggs Janet eats and bakes for herself each day.\n3. Find out how many eggs are left to be sold.\n4. Calculate the revenue from selling the remaining eggs at $2 per egg.\n\nLet's start with the first step:\n\n1. Janet's ducks lay 16 eggs per day.\n\nNext, we calculate how many eggs Janet eats and bakes for herself each day:\n\n2. Janet eats 3 eggs for breakfast every morning.\n3. Janet bakes 4 eggs for her friends every day.\n\nSo, the total number of eggs Janet eats and bakes for herself each day is:\n\\[ 3 + 4 = 7 \\text{ eggs} \\]\n\nNow, we find out how many eggs are left to be sold:\n\\[ 16 - 7 = 9 \\text{ eggs} \\]\n\nFinally, we calculate the revenue from selling the remaining eggs at $2 per egg:\n\\[ 9 \\times 2 = 18 \\text{ dollars} \\]\n\nTherefore, Janet makes boxed 18 dollars every day at the farmers' market."}
] # 3.75

conversation_str = tokenizer.apply_chat_template(
    chat, 
    tokenize=False, 
    add_generation_prompt=False
)

input_ids = tokenizer.encode(
    conversation_str, 
    return_tensors="pt", 
    add_special_tokens=False
).to(model.device)

outputs = model(input_ids=input_ids)
print(outputs[0])
