# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus
import dashscope


# get api: https://help.aliyun.com/zh/dashscope/developer-reference/activate-dashscope-and-create-an-api-key
dashscope.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# quick start: https://help.aliyun.com/zh/dashscope/create-a-chat-foundation-model
def sample_sync_call():
    prompt_text = '用萝卜、土豆、茄子做饭，给我个菜谱。'
    resp = dashscope.Generation.call(
        model='qwen-turbo',
        prompt=prompt_text,
    )
    
    if resp.status_code == HTTPStatus.OK:
        print(resp.output)  # The output text
        print(resp.usage)  # The usage information
    else:
        print(resp.code)  # The error code.
        print(resp.message)  # The error message.
        
        
def sample_sync_call_streaming():
    prompt_text = '用萝卜、土豆、茄子做饭，给我个菜谱。'
    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt=prompt_text,
        stream=True,
        top_p=0.8
    )

    for resp in response:
        if resp.status_code == HTTPStatus.OK:
            print(resp.output)  # The output text
            print(resp.usage)  # The usage information
        else:
            print(resp.code)  # The error code.
            print(resp.message)  # The error message.
    

def sample_sync_call_streaming_format():
    prompt_text = '用萝卜、土豆、茄子做饭，给我个菜谱。'
    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt=prompt_text,
        stream=True,
        top_p=0.8
    )
    
    head_idx = 0
    for resp in response:
        paragraph = resp.output['text']
        print("\r%s" % paragraph[head_idx:len(paragraph)], end='')
        if(paragraph.rfind('\n') != -1):
            head_idx = paragraph.rfind('\n') + 1

sample_sync_call()

sample_sync_call_streaming()

sample_sync_call_streaming_format()
