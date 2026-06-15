import streamlit as st
from datetime import date
import random

st.set_page_config(
    page_title="수행평가 알리미 뽑기",
    page_icon="📚",
    layout="centered"
)

st.title("📚 수행평가 알리미 뽑기")
st.caption("등록한 수행평가 중 오늘 할 과제를 랜덤으로 뽑아보세요!")

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 수행평가 추가
st.subheader("➕ 수행평가 등록")

with st.form("add_task"):
    subject = st.text_input("과목명")
    task_name = st.text_input("수행평가 이름")
    due_date = st.date_input("마감일", min_value=date.today())

    submitted = st.form_submit_button("등록")

    if submitted:
        try:
            if not subject.strip():
                st.error("과목명을 입력하세요.")
            elif not task_name.strip():
                st.error("수행평가 이름을 입력하세요.")
            else:
                st.session_state.tasks.append({
                    "subject": subject.strip(),
                    "task": task_name.strip(),
                    "due": due_date
                })
                st.success("수행평가가 등록되었습니다.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

st.divider()

# 목록 출력
st.subheader("📋 등록된 수행평가")

if st.session_state.tasks:
    sorted_tasks = sorted(
        st.session_state.tasks,
        key=lambda x: x["due"]
    )

    for idx, task in enumerate(sorted_tasks):
        days_left = (task["due"] - date.today()).days

        st.write(
            f"**{idx+1}. [{task['subject']}] {task['task']}** "
            f"(마감: {task['due']}, D-{days_left})"
        )

    nearest = min(st.session_state.tasks, key=lambda x: x["due"])

    st.info(
        f"⏰ 가장 급한 수행평가: "
        f"[{nearest['subject']}] {nearest['task']} "
        f"(마감 {nearest['due']})"
    )

else:
    st.warning("등록된 수행평가가 없습니다.")

st.divider()

# 랜덤 뽑기
st.subheader("🎲 오늘의 수행평가 뽑기")

if st.button("뽑기!"):
    try:
        if not st.session_state.tasks:
            st.warning("먼저 수행평가를 등록하세요.")
        else:
            selected = random.choice(st.session_state.tasks)

            st.success(
                f"""
                🎯 오늘의 수행평가

                과목: {selected['subject']}
                
                수행평가: {selected['task']}
                
                마감일: {selected['due']}
                """
            )

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.divider()

# 삭제 기능
st.subheader("🗑 수행평가 삭제")

if st.session_state.tasks:
    options = [
        f"[{t['subject']}] {t['task']}"
        for t in st.session_state.tasks
    ]

    selected_delete = st.selectbox(
        "삭제할 수행평가 선택",
        options
    )

    if st.button("삭제"):
        try:
            idx = options.index(selected_delete)
            st.session_state.tasks.pop(idx)
            st.success("삭제되었습니다.")
            st.rerun()
        except Exception as e:
            st.error(f"삭제 중 오류 발생: {e}")
