from openai import OpenAI

client = OpenAI(
    base_url="http://172.27.221.3:12000/v1",
    api_key="empty",
)

models = client.models.list()
model = models.data[0].id

print(model)

response = client.responses.create(
    model=model,
    input="Tell me a three sentence bedtime story about a unicorn."
)

print(response)