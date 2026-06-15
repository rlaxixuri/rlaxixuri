import streamlit as st
import random

st.set_page_config(
    page_title="수행평가 알리미 뽑기",
    page_icon="📢",
    layout="centered"
)

st.title("📢 수행평가 알리미 뽑기")

st.write(
    """
    수행평가 일정이나 준비물을
    선생님께 알리거나 친구들에게 공지할 담당자를
    랜덤으로 뽑아보세요!
    """
)

if "history" not in st.session_state:
    st.session_state.history = []

default_names = """김민수
이서준
박지호
최유진
정하준"""

names_text = st.text_area(
    "학생 이름 입력 (한 줄에 한 명)",
    value=default_names,
    height=200
)

col1, col2 = st.columns(2)

with col1:
    draw_button = st.button(
        "🎲 뽑기",
        use_container_width=True
    )

with col2:
    reset_button = st.button(
        "🗑 기록 초기화",
        use_container_width=True
    )

if reset_button:
    st.session_state.history = []
    st.success("기록이 초기화되었습니다.")

if draw_button:
    try:
        names = [
            name.strip()
            for name in names_text.split("\n")
            if name.strip()
        ]

        names = list(dict.fromkeys(names))

        if len(names) < 2:
            st.error("최소 2명 이상의 이름을 입력해주세요.")
        else:
            winner = random.choice(names)

            st.session_state.history.insert(0, winner)

            st.success("🎉 선정 완료!")

            st.markdown(
                f"""
                ## 📢 오늘의 수행평가 알리미

                # 🏆 {winner}
                """
            )

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.divider()

st.subheader("📋 이전 뽑기 기록")

if st.session_state.history:
    for idx, person in enumerate(
        st.session_state.history,
        start=1
    ):
        st.write(f"{idx}. {person}")
else:
    st.info("아직 뽑기 기록이 없습니다.")
