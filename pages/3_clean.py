# app.py

```python
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone, date

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="수행평가 정리함",
    page_icon="📚",
    layout="wide"
)

st.title("📚 수행평가 정리함")
st.write("수행평가를 등록하고 마감일을 한눈에 확인해보세요!")

# =========================
# 한국 시간 기준 오늘 날짜
# =========================
KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date()

# =========================
# 세션 상태 초기화
# =========================
if "assignments" not in st.session_state:
    st.session_state.assignments = []

# =========================
# 수행평가 등록 폼
# =========================
with st.form("assignment_form", clear_on_submit=True):
    st.subheader("➕ 수행평가 등록")

    title = st.text_input("수행평가 제목")
    subject = st.text_input("과목")

    due_date = st.date_input(
        "마감 날짜",
        min_value=today
    )

    importance = st.selectbox(
        "중요도",
        ["높음", "보통", "낮음"]
    )

    description = st.text_area(
        "상세 내용 (준비물, 제출 방식 등)"
    )

    submitted = st.form_submit_button("등록")

    if submitted:
        if not title.strip():
            st.error("수행평가 제목을 입력해주세요.")
        elif not subject.strip():
            st.error("과목을 입력해주세요.")
        else:
            st.session_state.assignments.append({
                "제목": title.strip(),
                "과목": subject.strip(),
                "마감일": due_date,
                "중요도": importance,
                "상세내용": description.strip(),
                "완료": False
            })

            st.success("수행평가가 등록되었습니다!")

# =========================
# 등록된 수행평가 목록
# =========================
st.divider()
st.subheader("📋 등록된 수행평가")

if not st.session_state.assignments:
    st.info("등록된 수행평가가 없습니다.")

else:
    # 원본 인덱스 유지
    assignment_list = []

    for i, item in enumerate(st.session_state.assignments):
        assignment_list.append({
            "원본인덱스": i,
            **item
        })

    df = pd.DataFrame(assignment_list)

    # 마감일 기준 정렬
    df = df.sort_values(by="마감일")

    for _, row in df.iterrows():

        original_index = row["원본인덱스"]

        days_left = (row["마감일"] - today).days

        if days_left == 0:
            d_day = "D-Day"
        elif days_left > 0:
            d_day = f"D-{days_left}"
        else:
            d_day = "마감 지남"

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"### {row['제목']}")

                st.write(f"**과목:** {row['과목']}")
                st.write(f"**마감일:** {row['마감일']}")
                st.write(f"**중요도:** {row['중요도']}")
                st.write(f"**남은 기간:** {d_day}")

                if days_left == 0:
                    st.error("🚨 오늘 마감인 수행평가입니다!")

                if row["상세내용"]:
                    st.write("**상세 내용**")
                    st.write(row["상세내용"])

            with col2:
                completed = st.checkbox(
                    "완료",
                    value=row["완료"],
                    key=f"complete_{original_index}"
                )

                st.session_state.assignments[original_index]["완료"] = completed

                if st.button(
                    "삭제",
                    key=f"delete_{original_index}"
                ):
                    st.session_state.assignments.pop(original_index)
                    st.rerun()

            if completed:
                st.success("✅ 완료한 수행평가")

# =========================
# 전체 삭제
# =========================
st.divider()

if st.session_state.assignments:
    if st.button("🗑️ 전체 삭제"):
        st.session_state.assignments = []
        st.rerun()
```
