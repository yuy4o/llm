from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12000/v1",
    api_key="empty",
)

models = client.models.list()
model = models.data[0].id

print(model)

completion = client.chat.completions.create(
  model= model,
  messages=[
    # {"role": "system", "content": ""},
    {"role": "user", "content": "hi"}
  ],
  temperature=0.7,
  max_tokens=4096,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None,
  stream=True,
  # extra_body={"chat_template_kwargs": {"enable_thinking": False}}
)

for chunk in completion:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end='')

# for chunk in completion:
#     print(chunk.choices[0].delta.content or "", end="")