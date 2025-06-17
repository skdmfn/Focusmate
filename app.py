import streamlit as st
from datetime import datetime, timedelta
import time

st.set_page_config(layout="wide", page_title="Focusmate")

st.markdown("""
<style>
h1, h2, h3 {
    color: #004578;
}
.todo-item {
    font-size: 18px;
    padding: 5px;
}
.timer {
    font-size: 48px;
    font-weight: bold;
    color: #d9534f;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Focusmate - Productivity Hub")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("✅ 할 일 목록")
    if 'todos' not in st.session_state:
        st.session_state.todos = []

    new_task = st.text_input("새 할 일 추가")
    if st.button("추가"):
        if new_task:
            st.session_state.todos.append({"task": new_task, "done": False})

    for i, todo in enumerate(st.session_state.todos):
        colA, colB = st.columns([0.1, 0.9])
        done = colA.checkbox("", value=todo["done"], key=f"done_{i}")
        text = f"~~{todo['task']}~~" if done else todo['task']
        colB.markdown(f"<div class='todo-item'>{text}</div>", unsafe_allow_html=True)
        st.session_state.todos[i]["done"] = done

with col2:
    st.header("⏲️ 집중 타이머")
    minutes = st.slider("타이머 설정 (분)", 1, 60, 25)
    if st.button("타이머 시작"):
        end_time = datetime.now() + timedelta(minutes=minutes)
        st.session_state.timer_end = end_time

    if "timer_end" in st.session_state:
        remaining = st.session_state.timer_end - datetime.now()
        if remaining.total_seconds() > 0:
            mins, secs = divmod(int(remaining.total_seconds()), 60)
            st.markdown(f"<div class='timer'>{mins:02}:{secs:02}</div>", unsafe_allow_html=True)
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.success("⏰ 타이머 종료! 잘 했어요!")
