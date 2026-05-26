import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="💩 똥피하기 게임", layout="centered")

st.title("💩 똥피하기 게임")
st.write("좌우 버튼으로 똥을 피해보세요!")

# 게임 크기
WIDTH = 7
HEIGHT = 10

# 세션 상태 초기화
if "player" not in st.session_state:
    st.session_state.player = WIDTH // 2

if "poop_x" not in st.session_state:
    st.session_state.poop_x = random.randint(0, WIDTH - 1)

if "poop_y" not in st.session_state:
    st.session_state.poop_y = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# -----------------------
# 이동 버튼
# -----------------------
col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("⬅️ 왼쪽"):
        if st.session_state.player > 0:
            st.session_state.player -= 1

with col3:
    if st.button("오른쪽 ➡️"):
        if st.session_state.player < WIDTH - 1:
            st.session_state.player += 1

# -----------------------
# 게임 진행
# -----------------------
if not st.session_state.game_over:

    # 똥 아래로 이동
    st.session_state.poop_y += 1

    # 충돌 체크
    if (
        st.session_state.poop_y == HEIGHT - 1
        and st.session_state.poop_x == st.session_state.player
    ):
        st.session_state.game_over = True

    # 점수 증가 + 새 똥 생성
    elif st.session_state.poop_y >= HEIGHT:
        st.session_state.score += 1
        st.session_state.poop_y = 0
        st.session_state.poop_x = random.randint(0, WIDTH - 1)

# -----------------------
# 게임 화면 출력
# -----------------------
board = []

for y in range(HEIGHT):
    row = ""

    for x in range(WIDTH):

        # 똥
        if x == st.session_state.poop_x and y == st.session_state.poop_y:
            row += "💩"

        # 플레이어
        elif y == HEIGHT - 1 and x == st.session_state.player:
            row += "😎"

        else:
            row += "⬜"

    board.append(row)

# 화면 출력
for row in board:
    st.markdown(f"## {row}")

# 점수
st.subheader(f"🏆 점수: {st.session_state.score}")

# 게임 오버
if st.session_state.game_over:
    st.error("💥 게임 오버!")

    if st.button("다시 시작"):
        st.session_state.player = WIDTH // 2
        st.session_state.poop_x = random.randint(0, WIDTH - 1)
        st.session_state.poop_y = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.rerun()

# 자동 새로고침
time.sleep(0.5)
st.rerun()
