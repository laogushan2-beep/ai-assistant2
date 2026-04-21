import streamlit as st
import requests
import json
from datetime import datetime

# ==================== 配置 ====================
import os
from dotenv import load_dotenv

# 自动寻找并加载同目录下的 .env 文件
# 加载本地 .env (云端会忽略这行)
load_dotenv()

# 尝试两种方式读取 Key (Streamlit 云端有时更喜欢 st.secrets)
# ✅ 正确写法：从环境里拿，代码里不出现 gsk_ 开头的字符
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# 在网页上显示调试信息 (测试完后可以删掉)
if not GROQ_API_KEY:
    st.error("🚨 警告：代码完全没读到 API Key！请检查 Secrets 拼写。")
else:
    # 只显示前 6 位，确保安全，同时让我们知道它确实读到了
    st.info(f"✅ 调试：Key 已加载 (开头为: {GROQ_API_KEY[:6]}...)")

def ask_ai(question):
    """调用AI获取回答"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        with st.spinner("AI思考中..."):
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"AI调用失败: {str(e)}"

# ==================== Streamlit 网页界面 ====================
st.set_page_config(page_title="AI助手", page_icon="🤖", layout="wide")

st.title("🤖 DawnJ的AI助手")
st.markdown("### AI聊天工具")

# 输入框
user_input = st.text_input("请输入你的问题：", placeholder="例如：狗波最爱吃什么？")

if st.button("发送", type="primary"):
    if user_input.strip():
        answer = ask_ai(user_input)
        st.write("**AI回答：**")
        st.write(answer)
    else:
        st.warning("请输入问题后再发送！")

# 侧边栏说明
with st.sidebar:
    st.header("使用说明")
    st.write("这是一个简单的网页版AI助手")
    st.write("你可以在这里直接提问")
    st.write("目前支持：")
    st.write("- 自由聊天")
    st.write("- 代码相关问题")
    st.write("- 学习问题解答")

st.caption("Powered by Groq + Streamlit")