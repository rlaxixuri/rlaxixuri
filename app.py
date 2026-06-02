import streamlit as st
from google import genai
from google.genai import types

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💕",
    layout="centered"
)

st.title("💕 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# -------------------
# API Key 로드
# -------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -------------------
# Gemini Client
# -------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -------------------
# 세션 상태 초기화
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n\n"
                "연애, 썸, 이별, 재회, 고백, 장거리 연애 등 "
                "무엇이든 편하게 상담해 주세요."
            )
        }
    ]

# -------------------
# 기존 대화 출력
# -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------
# 사용자 입력
# -------------------
prompt = st.chat_input("고민을 입력해 주세요")

if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini에 전달할 대화 구성
    history_text = ""

    for msg in st.session_state.messages:
        role = "사용자" if msg["role"] == "user" else "상담사"
        history_text += f"{role}: {msg['content']}\n"

    full_prompt = f"""
당신은 공감 능력이 뛰어난 전문 연애상담 코치입니다.

규칙:
- 친절하고 따뜻하게 답변
- 비난하지 말 것
- 현실적인 조언 제공
- 위험하거나 폭력적인 행동은 권장하지 말 것
- 답변은 한국어

대화 기록:
{history_text}

상담 답변:
"""

    with st.chat_message("assistant"):
        try:
            with st.spinner("생각 중..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=1000,
                    )
                )

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

        except Exception as e:
            error_msg = f"오류가 발생했습니다.\n\n{str(e)}"

            st.error(error_msg)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_msg
                }
            )

# -------------------
# 사이드바
# -------------------
with st.sidebar:

    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "대화가 초기화되었습니다 😊"
            }
        ]
        st.rerun()

    st.info(
        "GitHub → Streamlit Community Cloud로 "
        "배포 가능한 예제입니다."
    )
        
