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

# 初始化两个模型的状态
if 'current_model_left' not in st.session_state:
    st.session_state.current_model_left = list(MODELS.keys())[0]
if 'current_model_right' not in st.session_state:
    st.session_state.current_model_right = list(MODELS.keys())[1]

# 初始化两个 OpenAI 客户端
if 'client_left' not in st.session_state:
    st.session_state.client_left = OpenAI(
        api_key="empty",
        base_url=MODELS[st.session_state.current_model_left]
    )
if 'client_right' not in st.session_state:
    st.session_state.client_right = OpenAI(
        api_key="empty",
        base_url=MODELS[st.session_state.current_model_right]
    )

# 初始化两个对话历史
if "messages_left" not in st.session_state:
    st.session_state.messages_left = []
if "messages_right" not in st.session_state:
    st.session_state.messages_right = []

# 显示标题
st.title("💬 LLM Chat Comparison")

# 创建左右两列
left_col, right_col = st.columns(2)

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
    # 同时处理左右两侧的对话
    for side, client, messages in [
        ("left", st.session_state.client_left, st.session_state.messages_left),
        ("right", st.session_state.client_right, st.session_state.messages_right)
    ]:
        # 添加用户消息到历史
        messages.append({"role": "user", "content": prompt})
        
        # 获取对应的列
        col = left_col if side == "left" else right_col
        
        with col:
            with st.chat_message("user"):
                st.markdown(prompt)

            # 创建助手消息占位
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 创建流式响应
                stream = client.chat.completions.create(
                    model=st.session_state.current_model_left if side == "left" else st.session_state.current_model_right,
                    messages=[{"role": m["role"], "content": m["content"]} for m in messages],
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
            messages.append({"role": "assistant", "content": full_response})