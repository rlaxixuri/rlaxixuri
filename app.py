import streamlit as st
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="외모관리 앱",
    page_icon="✨",
    layout="centered"
)

# 제목
st.title("✨ 외모관리 앱")
st.write("매일 자기관리를 기록해보세요!")

# 오늘 날짜
today = datetime.today().strftime("%Y-%m-%d")
st.subheader(f"📅 오늘 날짜: {today}")

# ---------------------------
# 루틴 체크
# ---------------------------
st.header("✅ 오늘의 루틴")

water = st.checkbox("물 2L 마시기")
exercise = st.checkbox("운동하기")
skincare = st.checkbox("스킨케어 하기")
sleep = st.checkbox("7시간 이상 자기")

# 진행률 계산
count = sum([water, exercise, skincare, sleep])
progress = count / 4

st.progress(progress)
st.write(f"오늘의 달성률: {int(progress * 100)}%")

# ---------------------------
# 피부 상태
# ---------------------------
st.header("🧴 피부 상태 기록")

skin = st.selectbox(
    "오늘 피부 상태",
    ["좋음", "보통", "건조함", "트러블", "민감함"]
)

st.write(f"오늘 피부 상태: **{skin}**")

# ---------------------------
# 운동 기록
# ---------------------------
st.header("🏋️ 운동 기록")

exercise_type = st.selectbox(
    "운동 종류",
    ["헬스", "러닝", "요가", "홈트", "걷기"]
)

exercise_time = st.slider("운동 시간 (분)", 0, 180, 30)

st.write(f"{exercise_type} {exercise_time}분 완료!")

# ---------------------------
# 식단 기록
# ---------------------------
st.header("🥗 오늘 먹은 음식")

food = st.text_input("음식 입력")

if food:
    st.success(f"'{food}' 기록 완료!")

# ---------------------------
# 메모
# ---------------------------
st.header("📝 오늘의 메모")

memo = st.text_area("자유롭게 작성하세요")

if st.button("저장하기"):
    st.success("오늘 기록 저장 완료! ✨")

# ---------------------------
# 하단
# ---------------------------
st.markdown("---")
st.caption("Made with Streamlit ❤️")
