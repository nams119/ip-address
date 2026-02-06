import streamlit as st
import google.generativeai as genai
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Page Configuration
st.set_page_config(page_title="IP Formatter Bot", page_icon="🤖", layout="centered")


# --- Password Protection ---
def check_password():
    """Returns `True` if the user had the correct password."""

    # 1. Get password from secrets
    password = st.secrets.get("PASSWORD") or os.environ.get("PASSWORD")

    # If no password is set in secrets, allow access (or you can choose to block)
    # For safety, let's block if no password is set to urge the user to set one
    if not password:
        st.error("⚠️ 관리자 설정 필요: Secrets에 'PASSWORD'가 설정되지 않았습니다.")
        return False

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password has already been validated
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.text_input(
        "비밀번호를 입력하세요",
        type="password",
        key="password",
        on_change=password_entered,
    )

    if (
        "password_correct" in st.session_state
        and not st.session_state["password_correct"]
    ):
        st.error("❌ 비밀번호가 틀렸습니다. 다시 시도해주세요.")

    return False


if not check_password():
    st.stop()  # Stop execution if password is not correct
# ---------------------------

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
            # Requesting Code Block for clear formatting and handling invalid IPs
            system_prompt = """
            당신은 텍스트 정리 봇입니다. 
            사용자가 입력한 텍스트를 콤마(,)나 공백을 기준으로 줄바꿈(\n)하여 정리하세요.
            
            **규칙:**
            1. 입력된 내용이 유효한 IP 주소(0~255 사이의 숫자 4개)가 아닌 경우(예: `325.435...`), **반드시** 출력 결과 위에 다음 문구를 적어주세요:
               "⚠️ 이건 유효한 IP 주소가 아닌 것 같지만, 요청하신 대로 줄바꿈하여 정리해 드렸습니다."
            2. 그 다음, 정리된 내용을 반드시 **코드 블록(code block)** 형식으로 출력하세요.
            
            **출력 예시:**
            (유효하지 않은 값이 있는 경우)
            ⚠️ 이건 유효한 IP 주소가 아닌 것 같지만, 요청하신 대로 줄바꿈하여 정리해 드렸습니다.
            ```text
            325.435.4353.235
            23445.463.463.453
            ...
            ```
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
