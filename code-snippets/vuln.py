from openai import OpenAI
import requests
import time

def send_request(message):
    client = OpenAI(
        base_url="http://172.27.221.3:5008/v1",
        api_key="empty",
    )

    models = client.models.list()
    model = models.data[0].id

    completion = client.chat.completions.create(
    model= model,
    messages=[
        {"role": "system", "content": "你的任务是根据提供的漏洞信息，从用户的角度提三个用户最可能问的问题，并给出真实的答案"},
        {"role": "user", "content": message}
    ],
    temperature=0.7,
    max_tokens=4096,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    return completion.choices[0].message.content

message1 = '''
组件名称：Spring Boot（Java框架）
组件版本：2.7.0
漏洞编号：CVE-2023-34055
漏洞描述：VMware Spring Boot是美国威睿（VMware）公司的一套开源框架。
VMware Spring Boot 存在安全漏洞，该漏洞源于允许攻击者通过特制的HTTP请求导致拒绝服务（DOS）。受影响的产品和版本：Spring Boot 2.7.0至2.7.17版本，3.0.0至3.0.12版本，3.1.0至3.1.5版本。

根据以上信息，推荐3个用户可能感兴趣的问答对。
'''

message2 = '''
漏洞编号：CVE-2023-34055
漏洞描述：VMware Spring Boot是美国威睿（VMware）公司的一套开源框架。
VMware Spring Boot 存在安全漏洞，该漏洞源于允许攻击者通过特制的HTTP请求导致拒绝服务（DOS）。受影响的产品和版本：Spring Boot 2.7.0至2.7.17版本，3.0.0至3.0.12版本，3.1.0至3.1.5版本。

根据以上信息，推荐3个用户可能感兴趣的问答对。
'''

message3 = '''
组件名称：Express.js（Node.js框架）
组件版本：4.0.0
漏洞编号：CVE-2014-6393
漏洞名称：Joyent Node.js Express web framework 跨站脚本漏洞
漏洞描述：Joyent Node.js是美国Joyent公司的一套建立在Google V8 JavaScript引擎之上的网络应用平台。Express web framework是其中的一个轻量级Web框架。 
Joyent Node.js中的Express web framework 3.11之前的版本和4.5之前的4.x版本存在跨站脚本漏洞。远程攻击者可利用该漏洞注入任意的Web脚本或HTML。

根据以上信息，推荐3个用户可能感兴趣的问答对。
'''

message4 = '''
漏洞编号：CVE-2014-6393
漏洞名称：Joyent Node.js Express web framework 跨站脚本漏洞
漏洞描述：Joyent Node.js是美国Joyent公司的一套建立在Google V8 JavaScript引擎之上的网络应用平台。Express web framework是其中的一个轻量级Web框架。 
Joyent Node.js中的Express web framework 3.11之前的版本和4.5之前的4.x版本存在跨站脚本漏洞。远程攻击者可利用该漏洞注入任意的Web脚本或HTML。

根据以上信息，推荐3个用户可能感兴趣的问答对。
'''

print(send_request(message1))
print('-------------------')
print(send_request(message2))
print('-------------------')
print(send_request(message3))
print('-------------------')
print(send_request(message4))