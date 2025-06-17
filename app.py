import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Focusmate")

# 세션 상태 초기화
if 'timer_end' not in st.session_state:
    st.session_state.timer_end = None

st.title("⏲️ 집중 타이머")

minutes = st.slider("타이머 설정 (분)", 1, 60, 25)
if st.button("타이머 시작"):
    st.session_state.timer_end = datetime.now() + timedelta(minutes=minutes)

if st.session_state.timer_end:
    remaining = st.session_state.timer_end - datetime.now()
    total_seconds = remaining.total_seconds()

    if total_seconds > 0:
        mins, secs = divmod(int(total_seconds), 60)
        st.markdown(f"<h1 style='color:#d9534f;'>{mins:02}:{secs:02}</h1>", unsafe_allow_html=True)
        st.experimental_rerun()  # 들여쓰기 맞음
    else:
        st.success("⏰ 타이머 종료! 잘 했어요!")
        st.session_state.timer_end = None
