import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="수행평가 가정통신문 생성기",
    page_icon="📚",
    layout="wide"
)

st.title("📚 수행평가 가정통신문 생성기")
st.caption("다가오는 수행평가를 날짜순으로 정리하여 학부모와 학생에게 안내합니다.")

COLUMNS = ["과목", "수행평가명", "평가일", "준비물", "비고"]

if "schedule_df" not in st.session_state:
    st.session_state.schedule_df = pd.DataFrame(columns=COLUMNS)


def get_sample_data():
    return pd.DataFrame(
        [
            {
                "과목": "국어",
                "수행평가명": "독서 발표",
                "평가일": date(2026, 6, 20),
                "준비물": "발표 자료",
                "비고": "3분 발표"
            },
            {
                "과목": "과학",
                "수행평가명": "실험 보고서 제출",
                "평가일": date(2026, 6, 24),
                "준비물": "실험 노트",
                "비고": "개별 제출"
            },
            {
                "과목": "영어",
                "수행평가명": "영어 말하기",
                "평가일": date(2026, 6, 28),
                "준비물": "원고",
                "비고": "암기 필수"
            }
        ]
    )


with st.sidebar:
    st.header("⚙️ 관리 메뉴")

    uploaded_file = st.file_uploader(
        "CSV 업로드",
        type=["csv"],
        help="열 이름: 과목, 수행평가명, 평가일, 준비물, 비고"
    )

    if uploaded_file:
        try:
            uploaded_df = pd.read_csv(uploaded_file)

            required_cols = set(COLUMNS)

            if not required_cols.issubset(uploaded_df.columns):
                st.error("CSV 열 이름이 올바르지 않습니다.")

            else:
                uploaded_df["평가일"] = pd.to_datetime(
                    uploaded_df["평가일"]
                ).dt.date

                st.session_state.schedule_df = uploaded_df[COLUMNS]
                st.success("CSV를 불러왔습니다.")

        except Exception:
            st.error("CSV 파일 형식을 확인해주세요.")

    if st.button("샘플 데이터 불러오기"):
        st.session_state.schedule_df = get_sample_data()
        st.success("샘플 데이터를 불러왔습니다.")

    if st.button("전체 일정 초기화"):
        st.session_state.schedule_df = pd.DataFrame(columns=COLUMNS)
        st.success("초기화되었습니다.")


st.subheader("➕ 수행평가 등록")

with st.form("add_schedule"):
    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input("과목")

        exam_name = st.text_input("수행평가명")

        exam_date = st.date_input(
            "평가일",
            min_value=date.today()
        )

    with col2:
        materials = st.text_input("준비물")

        note = st.text_area("비고")

    submitted = st.form_submit_button("일정 추가")

    if submitted:
        if not subject.strip() or not exam_name.strip():
            st.warning("과목과 수행평가명을 입력해주세요.")

        else:
            new_row = pd.DataFrame(
                [
                    {
                        "과목": subject.strip(),
                        "수행평가명": exam_name.strip(),
                        "평가일": exam_date,
                        "준비물": materials.strip(),
                        "비고": note.strip()
                    }
                ]
            )

            st.session_state.schedule_df = pd.concat(
                [st.session_state.schedule_df, new_row],
                ignore_index=True
            )

            st.success("일정이 추가되었습니다.")


today = date.today()

df = st.session_state.schedule_df.copy()

if not df.empty:
    df["평가일"] = pd.to_datetime(df["평가일"]).dt.date

    upcoming_df = df[df["평가일"] >= today].copy()

    upcoming_df = upcoming_df.sort_values("평가일")

    if not upcoming_df.empty:

        upcoming_df["D-Day"] = upcoming_df["평가일"].apply(
            lambda x: (
                "오늘"
                if (x - today).days == 0
                else f"D-{(x - today).days}"
            )
        )

        st.subheader("🗓️ 예정된 수행평가")

        display_df = upcoming_df[
            ["D-Day", "평가일", "과목", "수행평가명", "준비물", "비고"]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv = upcoming_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="📥 일정 CSV 다운로드",
            data=csv,
            file_name="수행평가일정.csv",
            mime="text/csv"
        )

        st.subheader("🏠 가정통신문 미리보기")

        notice = (
            f"안녕하세요. 학부모님께 안내드립니다.\n\n"
            f"아래는 예정된 수행평가 일정입니다.\n"
            f"학생들이 미리 준비할 수 있도록 가정에서도 확인 부탁드립니다.\n\n"
        )

        for _, row in display_df.iterrows():
            notice += (
                f"• {row['평가일']} ({row['D-Day']})\n"
                f"  - 과목: {row['과목']}\n"
                f"  - 수행평가: {row['수행평가명']}\n"
                f"  - 준비물: {row['준비물'] or '-'}\n"
                f"  - 비고: {row['비고'] or '-'}\n\n"
            )

        notice += "감사합니다."

        st.text_area(
            "가정통신문 내용",
            value=notice,
            height=350
        )

    else:
        st.info("예정된 수행평가가 없습니다.")

else:
    st.info("등록된 수행평가가 없습니다. 일정을 추가해 주세요.")
