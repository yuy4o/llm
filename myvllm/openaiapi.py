from openai import OpenAI
client = OpenAI(
    base_url="http://172.27.33.63:1234/v1",
    api_key="LLMSec189!",
)

models = client.models.list()
model = models.data[0].id

print(model)

# # with open('1.txt', 'r', encoding='utf-8') as file:
# #     content = file.read()[:70000]
# #     # print(content)
# content = "武林至尊，宝刀屠龙"

# prompt = f'''根据以下文档的内容，回复用户的问题:
# {content}

# '''
# print(prompt)

completion = client.chat.completions.create(
  model= model,
  messages=[
    # {"role": "system", "content": prompt},
    {"role": "user", "content": "1+3="},
    {"role": "bot", "content": "4"},
    {"role": "user", "content": "1-3="}
  ],
  temperature=0.7,
  max_tokens=512,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)
print(completion)
print(completion.choices[0].message.content)