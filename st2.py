import streamlit as st
from openai import OpenAI
import time

# 配置页面
st.set_page_config(page_title="LLM Chat", layout="wide")

# 定义可用的模型
MODELS = {
    "/data/wenhr/modelhub/Qwen2.5-Coder-32B-Instruct": "http://localhost:8777/v1",
    "/data/wenhr/modelhub/QwQ-32B-Preview": "http://localhost:8778/v1"
}

# 初始化选中的模型
if 'current_model' not in st.session_state:
    st.session_state.current_model = list(MODELS.keys())[0]

# 初始化 OpenAI 客户端
if 'client' not in st.session_state:
    st.session_state.client = OpenAI(
        api_key="empty",
        base_url=MODELS[st.session_state.current_model]
    )

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示标题和模型选择
st.title("💬 LLM Chat")
selected_model = st.selectbox("选择模型", options=list(MODELS.keys()), index=list(MODELS.keys()).index(st.session_state.current_model))

# 如果模型改变，更新客户端
if selected_model != st.session_state.current_model:
    st.session_state.current_model = selected_model
    st.session_state.client = OpenAI(
        api_key="empty",
        base_url=MODELS[selected_model]
    )
    st.session_state.messages = []  # 清空聊天历史
    st.rerun()

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
            model=st.session_state.current_model,  # 使用当前选中的模型
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