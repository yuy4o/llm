import sys
import requests
import time
import json

def send_request():
    url = 'http://172.27.221.3:8777/api/local_doc_qa/local_doc_chat'
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "user_id": "zzp",
        "kb_ids": ['KB8523fd4d18374601ac3d5464e37219fd', 'KB8523fd4d18374601ac3d5464e37219fd_FAQ'],
        "question": '''结合公式分类别详细回答以下的问题：\
        问题一：软件物料清单里提到了哪些要求？\
        问题二：什么是暴露面资产?辽宁公司的互联网暴露面资产包含哪些？ \
        问题三：常见的漏洞有哪些类型？针对不同类型有哪些应对措施？
        ''',
    }
    try:
        start_time = time.time()
        response = requests.post(url=url, headers=headers, json=data, timeout=60)
        end_time = time.time()
        res = response.json()
        
        ress = json.dumps(res)
        with open('1.json', 'w') as file:
            file.write(ress)            
        print(f"响应状态码: {response.status_code}, 响应时间: {end_time - start_time}秒")
    except Exception as e:
        print(f"请求发送失败: {e}")


if __name__ == '__main__':
    send_request()