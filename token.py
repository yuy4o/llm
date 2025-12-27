# 挂载云盘
from google.colab import drive
drive.mount('/content/drive')

# huggingface authorization
from huggingface_hub import login
login(token="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation import GenerationConfig

MODEL_NAME_OR_PATH = "Qwen/Qwen2-1.5B"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME_OR_PATH, 
    trust_remote_code=True)

messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}
]

encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

print(encodeds)

device = "cuda"
model_inputs = encodeds.to(device)
model.to(device)

generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME_OR_PATH,
    device_map="cuda:0",
    trust_remote_code=True)

generation_config = GenerationConfig.from_pretrained(
    MODEL_NAME_OR_PATH,
    trust_remote_code=True)

inputs = tokenizer('2**4=', return_tensors='pt')
inputs = inputs.to(model.device)

pred = model.generate(input_ids=inputs["input_ids"], generation_config=generation_config)
print("outputs:\n", tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))


######## bert embedding ###########
import torch
from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')
input_ids = torch.tensor(tokenizer.encode('你好')).unsqueeze(0)
outputs = model(input_ids)

outputs[0].shape, outputs[1].shape #字向量 词向量
input_ids #<CLS>101 <SEP>102


########查看不同模型的分词###########
def get_tokenization(model_name, text):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    return tokens

text = "你好，世界！"
models = ["gpt2", "bert-base-chinese", "t5-small", "meta-llama/Meta-Llama-3-8B"]

for model in models:
    tokens = get_tokenization(model, text)
    print(f"Model: {model}")
    print(f"Tokens: {tokens}")
    print(f"Token数量: {len(tokens)}\n")