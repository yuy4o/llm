import streamlit as st
from openai import OpenAI
import time

# 配置页面
st.set_page_config(page_title="LLM Chat", layout="wide")

# 定义可用的模型
MODELS = {
    "/data/wenhr/modelhub/Qwen2.5-Coder-32B-Instruct": "http://localhost:8777/v1",
    "/data/wenhr/modelhub/QwQ-32B-Preview": "http://localhost:8778/v1",
    "/data/wenhr/modelhub/DeepSeek-R1-Distill-Qwen-32B": "http://localhost:7777/v1"
}

# 初始化三个模型的状态
if 'current_model_left' not in st.session_state:
    st.session_state.current_model_left = list(MODELS.keys())[0]
if 'current_model_middle' not in st.session_state:
    st.session_state.current_model_middle = list(MODELS.keys())[1]
if 'current_model_right' not in st.session_state:
    st.session_state.current_model_right = list(MODELS.keys())[2]

# 初始化三个 OpenAI 客户端
if 'client_left' not in st.session_state:
    st.session_state.client_left = OpenAI(
        api_key="empty",
        base_url=MODELS[st.session_state.current_model_left]
    )
if 'client_middle' not in st.session_state:
    st.session_state.client_middle = OpenAI(
        api_key="empty",
        base_url=MODELS[st.session_state.current_model_middle]
    )
if 'client_right' not in st.session_state:
    st.session_state.client_right = OpenAI(
        api_key="empty",
        base_url=MODELS[st.session_state.current_model_right]
    )

# 初始化三个对话历史
if "messages_left" not in st.session_state:
    st.session_state.messages_left = []
if "messages_middle" not in st.session_state:
    st.session_state.messages_middle = []
if "messages_right" not in st.session_state:
    st.session_state.messages_right = []

# 显示标题
st.title("💬 LLM Chat Comparison")

# 创建三列
left_col, middle_col, right_col = st.columns(3)

# 左侧列
with left_col:
    selected_model_left = st.selectbox(
        "选择左侧模型",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.current_model_left),
        key="left_model"
    )
    
    if selected_model_left != st.session_state.current_model_left:
        st.session_state.current_model_left = selected_model_left
        st.session_state.client_left = OpenAI(
            api_key="empty",
            base_url=MODELS[selected_model_left]
        )
        st.session_state.messages_left = []
        st.rerun()

    # 显示左侧聊天历史
    for message in st.session_state.messages_left:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 中间列
with middle_col:
    selected_model_middle = st.selectbox(
        "选择中间模型",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.current_model_middle),
        key="middle_model"
    )
    
    if selected_model_middle != st.session_state.current_model_middle:
        st.session_state.current_model_middle = selected_model_middle
        st.session_state.client_middle = OpenAI(
            api_key="empty",
            base_url=MODELS[selected_model_middle]
        )
        st.session_state.messages_middle = []
        st.rerun()

    # 显示中间聊天历史
    for message in st.session_state.messages_middle:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 右侧列
with right_col:
    selected_model_right = st.selectbox(
        "选择右侧模型",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.current_model_right),
        key="right_model"
    )
    
    if selected_model_right != st.session_state.current_model_right:
        st.session_state.current_model_right = selected_model_right
        st.session_state.client_right = OpenAI(
            api_key="empty",
            base_url=MODELS[selected_model_right]
        )
        st.session_state.messages_right = []
        st.rerun()

    # 显示右侧聊天历史
    for message in st.session_state.messages_right:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("What's up?"):
    # 创建线程安全的变量来存储响应
    responses = {'left': '', 'middle': '', 'right': ''}
    message_placeholders = {}
    
    # 在主线程中创建UI元素
    for side in ['left', 'middle', 'right']:
        col = left_col if side == "left" else (middle_col if side == "middle" else right_col)
        with col:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholders[side] = st.empty()
    
    # 在创建线程前获取模型信息
    model_info = {
        'left': st.session_state.current_model_left,
        'middle': st.session_state.current_model_middle,
        'right': st.session_state.current_model_right
    }
    
    def generate_response(side, client, messages, model_name):
        # 添加用户消息到历史
        messages.append({"role": "user", "content": prompt})
        
        # 创建流式响应
        stream = client.chat.completions.create(
            model=model_name,  # 使用传入的模型名称
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
            stream=True,
            temperature=0.7,
        )
        
        # 逐字显示回复
        response = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                responses[side] = response
                time.sleep(0.01)
        
        # 添加助手消息到历史
        messages.append({"role": "assistant", "content": response})
    
    import threading
    
    # 创建三个线程
    threads = []
    for side, client, messages in [
        ("left", st.session_state.client_left, st.session_state.messages_left),
        ("middle", st.session_state.client_middle, st.session_state.messages_middle),
        ("right", st.session_state.client_right, st.session_state.messages_right)
    ]:
        thread = threading.Thread(
            target=generate_response,
            args=(side, client, messages, model_info[side])
        )
        threads.append(thread)
        thread.start()
    
    # 在响应生成过程中更新UI
    while any(thread.is_alive() for thread in threads):
        for side in ['left', 'middle', 'right']:
            message_placeholders[side].markdown(responses[side] + "▌")
        time.sleep(0.1)
    
    # 显示最终响应
    for side in ['left', 'middle', 'right']:
        message_placeholders[side].markdown(responses[side])
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()