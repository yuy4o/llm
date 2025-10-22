# from openai import OpenAI
# import json

# file_path = 'python_entry_202407181557.csv'
# data_list = []

# with open(file_path, 'r') as file:
#     for line in file:
#         data_list.append(line.strip())

# data_list = data_list[:100000]

# # print(data_list)
# print(len(data_list))

# with open('result.txt', 'a') as file:
#   for i in range(0, len(data_list)):
#     text = data_list[i]
#     # # 注意，结果仅以json的格式生成字符串；不要额外添加其他格式，例如markdown规范的各种字符等等；不能生成不符合json格式的结果；生成的结果要能够直接用python代码加载为dict对象。
#     message = [
#       {"role": "user", "content": f'''
#           你是一个经验丰富的工程师，分析并判断 {text} 是否和机器学习或深度学习高度相关。进行内容标注，相关标注1，不相关标注0。不要改变和扩充{text}的内容。不要解释任何原因。返回形式需要参考### 示例 ###的格式。
#           ### 示例 ###
#           "00000000", 0
#           "afc-svm-imbalanced-learning", 1
#       '''},
#     ]

#     client = OpenAI(
#         base_url="http://localhost:5003/v1",
#         api_key="LLMSec189!",
#     )

#     models = client.models.list()
#     model = models.data[0].id

#     completion = client.chat.completions.create(
#       model= model,
#       messages= message,
#       temperature=0.7,
#       max_tokens=4096,
#       top_p=0.95,
#       frequency_penalty=0,
#       presence_penalty=0,
#       stop=None
#     )

#     print(completion.choices[0].message.content)

#     file.write(completion.choices[0].message.content)
#     file.write('\n')
# ----------------------------------------------------------

# import json
# from openai import OpenAI
# import concurrent.futures

# file_path = 'python_entry_202407181557.csv'
# data_list = []

# with open(file_path, 'r') as file:
#     for line in file:
#         data_list.append(line.strip())

# data_list = data_list[4850:]

# client = OpenAI(
#     base_url="http://localhost:5003/v1",
#     api_key="LLMSec189!"
# )

# models = client.models.list()
# model = models.data[0].id

# def process_text(text):
#     message = [
#         {"role": "user", "content": f'''
#             你是一个经验丰富的工程师，分析并判断 {text} 是否和机器学习或深度学习高度相关。进行内容标注，相关标注1，不相关标注0。不要改变和扩充{text}的内容。不要解释任何原因。返回形式需要参考### 示例 ###的格式。
#             ### 示例 ###
#             "00000000", 0
#             "afc-svm-imbalanced-learning", 1
#         '''}
#     ]

#     completion = client.chat.completions.create(
#         model=model,
#         messages=message,
#         temperature=0.7,
#         max_tokens=4096,
#         top_p=0.95,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=None
#     )

#     return completion.choices[0].message.content

# def main():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=14) as executor:
#         results = list(executor.map(process_text, data_list))

#     with open('result.txt', 'a') as file:
#         for result in results:
#             file.write(result)
#             file.write('\n')

# if __name__ == "__main__":
#     main()

# ----------------------------------------------------------

# import json
# from openai import OpenAI
# import concurrent.futures
# from tqdm import tqdm

# file_path = 'python_entry_202407181557.csv'
# data_list = []

# with open(file_path, 'r') as file:
#     for line in file:
#         data_list.append(line.strip())

# data_list = data_list[4850:]  # 10000S /60 

# client = OpenAI(
#     base_url="http://localhost:5003/v1",
#     api_key="LLMSec189!"
# )

# models = client.models.list()
# model = models.data[0].id

# def process_text(text):
#     message = [
#         {"role": "user", "content": f'''
#             你是一个经验丰富的工程师，分析并判断 {text} 是否和机器学习或深度学习高度相关。进行内容标注，相关标注1，不相关标注0。不要改变和扩充{text}的内容。不要解释任何原因。返回形式需要参考### 示例 ###的格式。
#             ### 示例 ###
#             "00000000", 0
#             "afc-svm-imbalanced-learning", 1
#         '''}
#     ]

#     completion = client.chat.completions.create(
#         model=model,
#         messages=message,
#         temperature=0.7,
#         max_tokens=4096,
#         top_p=0.95,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=None
#     )

#     return completion.choices[0].message.content

# def main():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=14) as executor:
#         results = list(tqdm(executor.map(process_text, data_list), total=len(data_list)))

#     with open('result.txt', 'a') as file:
#         for result in results:
#             file.write(result)
#             file.write('\n')

# if __name__ == "__main__":
#     main()


# ----------------------------------------------------------


import json
from openai import OpenAI
import concurrent.futures
from tqdm import tqdm
from threading import Lock

file_path = 'python_entry_202407181557.csv'
data_list = []

with open(file_path, 'r') as file:
    for line in file:
        data_list.append(line.strip())

data_list = data_list[7292:]

client = OpenAI(
    base_url="http://localhost:5003/v1",
    api_key="LLMSec189!"
)

models = client.models.list()
model = models.data[0].id

lock = Lock()

def process_text(text):
    message = [
        {"role": "user", "content": f'''
            你是一个经验丰富的工程师，分析并判断 {text} 是否和机器学习或深度学习高度相关。进行内容标注，相关标注1，不相关标注0。不要改变和扩充{text}的内容。不要解释任何原因。返回形式需要参考### 示例 ###的格式。
            ### 示例 ###
            "00000000", 0
            "afc-svm-imbalanced-learning", 1
        '''}
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=0.7,
        max_tokens=4096,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    result = completion.choices[0].message.content
    result = result.replace('"','') #最后修改

    with lock:
        with open('result.txt', 'a') as file:
            file.write(result)
            file.write('\n')

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=48) as executor:
        list(tqdm(executor.map(process_text, data_list), total=len(data_list)))

if __name__ == "__main__":
    main()
