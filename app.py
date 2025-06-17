import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Focusmate", layout="centered")

# 초기 상태값 설정
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'task_input' not in st.session_state:
    st.session_state.task_input = ""

if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

if 'timer_length' not in st.session_state:
    st.session_state.timer_length = 25  # 기본 25분

# 투두 리스트 함수
def add_task():
    task = st.session_state.task_input.strip()
    if task:
        st.session_state.tasks.append(task)
        st.session_state.task_input = ""

def remove_task(idx):
    st.session_state.tasks.pop(idx)

# 타이머 함수
def start_timer():
    st.session_state.timer_start = datetime.now()

def reset_timer():
    st.session_state.timer_start = None

# UI 구성
st.title("🎯 Focusmate - 집중 생산성 앱")

# 투두 리스트 영역
st.header("✅ 할 일 목록")

col1, col2 = st.columns([3,1])

with col1:
    st.text_input("새 작업 추가", key="task_input", on_change=add_task)
    for i, task in enumerate(st.session_state.tasks):
        task_col1, task_col2 = st.columns([8,1])
        with task_col1:
            st.write(f"- {task}")
        with task_col2:
            if st.button("❌", key=f"del_{i}"):
                remove_task(i)
                st.experimental_rerun()

with col2:
    st.write("")

# 타이머 영역
st.header("⏲️ 집중 타이머")

st.session_state.timer_length = st.slider("타이머 설정 (분)", 1, 60, st.session_state.timer_length)

if st.session_state.timer_start is None:
    if st.button("타이머 시작"):
        start_timer()
        st.experimental_rerun()
else:
    elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
    remaining = st.session_state.timer_length * 60 - elapsed

    if remaining > 0:
        mins, secs = divmod(int(remaining), 60)
        st.markdown(f"<h1 style='color:#d9534f;'>{mins:02}:{secs:02}</h1>", unsafe_allow_html=True)
        if st.button("타이머 리셋"):
            reset_timer()
            st.experimental_rerun()
    else:
        st.success("⏰ 타이머 종료! 잘 했어요!")
        if st.button("다시 시작"):
            start_timer()
            st.experimental_rerun()
        if st.button("리셋"):
            reset_timer()
            st.experimental_rerun()
