import streamlit as st
import google.generativeai as genai
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Page Configuration
st.set_page_config(page_title="IP Formatter Bot", page_icon="🤖", layout="centered")

# Title and Description
st.title("🤖 IP Address Formatter")
st.markdown(
    """
IP 주소 목록을 입력하면 깔끔하게 정렬해드립니다.
예시: `123.45.67.89, 98.76.54.32` -> 줄바꿈으로 정리
"""
)

# API Key Configuration
# Try to get API key from Streamlit secrets (for cloud) or environment variable (for local)
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    # If not found, show an input field for local testing convenience
    with st.expander("API Key 설정 (로컬 테스트용)"):
        api_key = st.text_input("Google API Key를 입력하세요", type="password")
        if not api_key:
            st.info(
                "실행을 위해 API Key가 필요합니다. `.streamlit/secrets.toml`에 설정하거나 여기에 입력하세요."
            )
            st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    # Using the requested model
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    st.error(f"모델 설정 중 오류가 발생했습니다: {e}")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Add initial greeting
    # st.session_state.messages.append({
    #     "role": "assistant",
    #     "content": "안녕하세요! 정리하고 싶은 IP 주소들을 입력해주세요. 콤마(,)로 구분된 긴 IP 목록도 깔끔하게 줄바꿈하여 정리해 드립니다."
    # })

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("IP 주소 목록을 입력하세요..."):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # System instruction embedded in the prompt for simplicity in this single-turn use case
            # Requesting Code Block for clear formatting
            system_prompt = """
            당신은 IP 주소 정리 봇입니다. 
            사용자가 입력한 텍스트에서 IP 주소들을 추출하여, 각 IP 주소를 한 줄에 하나씩 출력하세요.
            
            반드시 아래와 같은 **코드 블록(code block)** 형식으로 출력하세요.
            ```text
            IP_ADDRESS_1
            IP_ADDRESS_2
            ...
            ```
            
            불필요한 설명이나 인삿말은 생략하고 결과만 출력하세요.
            """

            chat = model.start_chat()
            response = chat.send_message(f"{system_prompt}\n\n사용자 입력:\n{prompt}")

            full_response = response.text
            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"오류가 발생했습니다: {e}"
            message_placeholder.error(full_response)

        # Add assistant response to history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
