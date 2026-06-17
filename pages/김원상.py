import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="수행평가 단톡방",
    page_icon="📚",
    layout="wide"
)

st.title("📚 수행평가 단톡방")
st.caption("수행평가 팀원들과 소통하고 역할을 관리하는 단톡방")

# -----------------------------
# Session State 초기화
# -----------------------------
if "members" not in st.session_state:
    st.session_state.members = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "notice" not in st.session_state:
    st.session_state.notice = "아직 공지사항이 없습니다."

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("👤 참가하기")

    nickname = st.text_input("닉네임")

    if st.button("참가"):
        try:
            if nickname.strip() == "":
                st.warning("닉네임을 입력하세요.")
            elif nickname in st.session_state.members:
                st.warning("이미 참가한 닉네임입니다.")
            else:
                st.session_state.members.append(nickname)
                st.success(f"{nickname}님 참가 완료!")
        except Exception:
            st.error("참가 중 오류가 발생했습니다.")

    st.divider()

    st.subheader("👥 참가 인원")
    if st.session_state.members:
        for member in st.session_state.members:
            st.write(f"• {member}")
    else:
        st.info("아직 참가한 사람이 없습니다.")

# -----------------------------
# 공지사항
# -----------------------------
st.subheader("📢 공지사항")

new_notice = st.text_area(
    "공지 수정",
    value=st.session_state.notice,
    height=100
)

if st.button("공지 저장"):
    try:
        st.session_state.notice = new_notice
        st.success("공지사항이 저장되었습니다.")
    except Exception:
        st.error("공지 저장 중 오류가 발생했습니다.")

st.info(st.session_state.notice)

st.divider()

# -----------------------------
# 역할 분담
# -----------------------------
st.subheader("✅ 역할 분담")

col1, col2 = st.columns(2)

with col1:
    task_name = st.text_input("역할/업무")
with col2:
    task_member = st.selectbox(
        "담당자",
        options=["미정"] + st.session_state.members
    )

if st.button("역할 추가"):
    try:
        if task_name.strip():
            st.session_state.tasks.append({
                "업무": task_name,
                "담당자": task_member,
                "상태": "진행중"
            })
            st.success("역할이 추가되었습니다.")
        else:
            st.warning("업무를 입력하세요.")
    except Exception:
        st.error("추가 중 오류가 발생했습니다.")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([3, 2, 2])

        cols[0].write(task["업무"])
        cols[1].write(task["담당자"])

        new_status = cols[2].selectbox(
            f"상태{i}",
            ["진행중", "완료"],
            index=0 if task["상태"] == "진행중" else 1,
            label_visibility="collapsed"
        )

        st.session_state.tasks[i]["상태"] = new_status
else:
    st.info("등록된 역할이 없습니다.")

st.divider()

# -----------------------------
# 채팅
# -----------------------------
st.subheader("💬 단톡방 채팅")

chat_name = st.selectbox(
    "보내는 사람",
    options=st.session_state.members if st.session_state.members else ["참가자 없음"]
)

chat_text = st.text_input("메시지 입력")

if st.button("전송"):
    try:
        if not st.session_state.members:
            st.warning("먼저 참가자를 추가하세요.")
        elif chat_text.strip() == "":
            st.warning("메시지를 입력하세요.")
        else:
            st.session_state.messages.append({
                "name": chat_name,
                "message": chat_text,
                "time": datetime.now().strftime("%H:%M")
            })
            st.success("전송 완료!")
    except Exception:
        st.error("메시지 전송 중 오류가 발생했습니다.")

st.markdown("### 채팅 기록")

if st.session_state.messages:
    for msg in reversed(st.session_state.messages):
        st.markdown(
            f"""
            **{msg['name']}** ({msg['time']})
            
            {msg['message']}
            ---
            """
        )
else:
    st.info("아직 채팅이 없습니다.")

st.divider()

# -----------------------------
# 진행 현황
# -----------------------------
st.subheader("📊 수행평가 진행 현황")

if st.session_state.tasks:
    total = len(st.session_state.tasks)
    completed = sum(
        1 for task in st.session_state.tasks
        if task["상태"] == "완료"
    )

    progress = completed / total
    st.progress(progress)

    st.write(f"완료: {completed} / {total}")
else:
    st.info("역할을 추가하면 진행률이 표시됩니다.")
