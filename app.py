import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.title("💬 포도미디어 상담봇")
st.write(
    "안녕하세요! 포도미디어 고객 상담봇입니다. "
    "중소기업 광고 마케팅 서비스에 대한 문의나 도움이 필요하시면 언제든지 말씀해주세요. "
    "자세한 정보는 [포도미디어 홈페이지](http://www.podooh.com/)를 방문해주세요."
)

# OpenAI API 키를 secrets.toml에서 가져옵니다.
openai_api_key = st.secrets["openai_api_key"]
if not openai_api_key:
    st.error("OpenAI API 키가 설정되어 있지 않습니다.", icon="🗝️")
    st.stop()

# API 키 유효성 검증
try:
    client = OpenAI(api_key=openai_api_key)
    # 간단한 API 호출로 키 검증
    client.models.list()
    st.success("API 키가 정상적으로 작동합니다.")
except Exception as e:
    st.error(f"API 키 검증 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# 세션 상태 변수에 채팅 메시지를 저장합니다.
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 시스템 메시지 추가 (상담봇의 역할 정의)
    st.session_state.messages.append({
        "role": "system",
        "content": "당신은 포도미디어의 친절한 상담봇입니다. "
                   "중소기업의 광고 마케팅 서비스에 대한 정보와 지원을 제공합니다."
    })

# 기존 채팅 메시지를 표시합니다 (시스템 메시지는 제외)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 채팅 입력 필드를 생성하여 사용자의 메시지를 받습니다.
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    # 현재 프롬프트를 저장하고 표시합니다.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API를 사용하여 응답을 생성합니다.
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True,
    )

    # 응답을 스트림으로 표시하고 세션 상태에 저장합니다.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
