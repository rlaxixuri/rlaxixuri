import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="수행평가 일정표",
    page_icon="📚",
    layout="centered"
)

st.title("📚 수행평가 일정표 만들기")
st.write("수행평가 일정을 입력하고 출력해보세요!")

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# 입력 폼
# -----------------------------
with st.form("task_form"):

    subject = st.text_input("과목")
    task = st.text_input("수행평가 내용")
    date = st.date_input("제출 날짜")
    memo = st.text_input("메모")

    submit = st.form_submit_button("추가하기")

    if submit:

        if subject and task:
            st.session_state.tasks.append({
                "과목": subject,
                "수행평가": task,
                "제출일": date,
                "메모": memo
            })

            st.success("일정이 추가되었습니다!")

        else:
            st.warning("과목과 수행평가 내용을 입력해주세요.")

# -----------------------------
# 일정표 출력
# -----------------------------
st.markdown("---")
st.subheader("🗓️ 수행평가 일정표")

if st.session_state.tasks:

    df = pd.DataFrame(st.session_state.tasks)

    # 날짜순 정렬
    df = df.sort_values(by="제출일")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # CSV 다운로드
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 일정표 다운로드 (CSV)",
        data=csv,
        file_name="수행평가_일정표.csv",
        mime="text/csv"
    )

    st.info("💡 Ctrl + P 를 누르면 프린트할 수 있어요!")

else:
    st.write("아직 입력된 일정이 없습니다.")

# -----------------------------
# 전체 삭제
# -----------------------------
if st.button("🗑️ 전체 삭제"):

    st.session_state.tasks = []
    st.rerun()

# -----------------------------
# 하단
# -----------------------------
st.markdown("---")
st.caption("Made with Streamlit ❤️")
