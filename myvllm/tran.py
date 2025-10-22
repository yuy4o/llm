import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"

tokenizer = AutoTokenizer.from_pretrained("./glm-4-9b-chat",trust_remote_code=True)

prompt = [{"role": "user", "content": 'x=3,x-3='}, {"role": "bot", "content": '0'},{"role": "user", "content": 'x+100='}]

inputs = tokenizer.apply_chat_template(prompt,
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       )

inputs = inputs.to(device)
model = AutoModelForCausalLM.from_pretrained(
    "./glm-4-9b-chat-1m",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).to(device).eval()

gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
with torch.no_grad():
    print("inputs:",inputs)
    print("gen_kwargs",gen_kwargs)
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
