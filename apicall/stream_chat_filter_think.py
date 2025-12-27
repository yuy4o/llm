from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12000/v1",
    api_key="empty"
)

models = client.models.list()
model = models.data[0].id

stream = client.chat.completions.create(
    model = model,
    temperature=0.6,
    max_tokens=2000,
    stream=True,
    messages=[
    # {"role": "system", "content": ""},
    {"role": "user", "content": "hi"}
  ]
)

inside_think = False
skip_leading_newline = True

for chunk in stream:
    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta
    if not delta or not delta.content:
        continue

    text = delta.content

    # 进入 think
    if "<think>" in text:
        inside_think = True
        continue

    # 退出 think
    if "</think>" in text:
        inside_think = False
        skip_leading_newline = True
        continue

    # think 中内容直接丢弃
    if inside_think:
        continue

    # 丢弃 think 后的前置换行
    if skip_leading_newline:
        if text.strip() == "":
            continue
        skip_leading_newline = False

    print(text, end="", flush=True)

print()