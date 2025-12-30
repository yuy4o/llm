# 页面一个窗口，单模型
import streamlit as st
from openai import OpenAI
import time

# 配置页面
st.set_page_config(page_title="LLM Chat", layout="wide")

# 初始化 OpenAI 客户端
if 'client' not in st.session_state:
    st.session_state.client = OpenAI(
        api_key="empty",  # 如果使用开源模型API，可以是任意值
        base_url="http://localhost:12000/v1"  # 替换为你的模型API地址
    )

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示标题
st.title("💬 LLM Chat")

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("What's up?"):
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 创建助手消息占位
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 创建流式响应
        stream = st.session_state.client.chat.completions.create(
            model="Qwen3-14B",  # 模型名称，根据你的API要求设置
            messages=[{"role": m["role"], "content": m["content"]} 
                     for m in st.session_state.messages],
            stream=True,
            temperature=0.7,
        )
        
        # 逐字显示回复
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
        
        # 显示完整回复
        message_placeholder.markdown(full_response)
    
    # 添加助手消息到历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})