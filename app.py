import streamlit as st
from datetime import date, datetime, timedelta
import time

st.set_page_config(page_title="Focusmate - 집중 생산성 앱", page_icon="🎯", layout="centered")

# CSS 스타일
st.markdown(
    """
    <style>
    .app-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #4B6EAF;
        margin-bottom: 1.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .task-item {
        background: #F3F6FD;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgb(75 110 175 / 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .task-text {
        font-size: 1.1rem;
        flex-grow: 1;
        margin-left: 0.7rem;
        color: #2F3E63;
    }
    .due-date {
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        min-width: 110px;
        text-align: center;
        user-select: none;
    }
    .due-normal {
        background-color: #A8C1FF;
        color: #1D2E69;
    }
    .due-soon {
        background-color: #FFBD59;
        color: #5C3900;
    }
    .due-past {
        background-color: #FF5C5C;
        color: #570000;
    }
    .delete-btn {
        cursor: pointer;
        font-size: 1.2rem;
        margin-left: 1rem;
        color: #A83C3C;
        transition: color 0.2s ease;
        user-select: none;
    }
    .delete-btn:hover {
        color: #FF0000;
    }
    .input-area {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .add-btn {
        background-color: #4B6EAF;
        border: none;
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .add-btn:hover {
        background-color: #3A5490;
    }
    .timer-container {
        background: #E9F0FF;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 3px 7px rgb(75 110 175 / 0.3);
        max-width: 400px;
        margin: 2rem auto 0 auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    .timer-display {
        font-size: 3rem;
        font-weight: 700;
        color: #2F3E63;
        margin-bottom: 1rem;
        letter-spacing: 0.15em;
    }
    .timer-buttons button {
        background-color: #4B6EAF;
        border: none;
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        margin: 0 0.5rem;
        transition: background-color 0.3s ease;
    }
    .timer-buttons button:hover {
        background-color: #3A5490;
    }
    .timer-select {
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-header">🎯 Focusmate - 집중 생산성 앱</div>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'timer_seconds' not in st.session_state:
    st.session_state.timer_seconds = 0

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'timer_end_time' not in st.session_state:
    st.session_state.timer_end_time = None

# 할 일 입력 및 마감일 선택
with st.form(key='task_form'):
    cols = st.columns([4, 2, 1])
    task_input = cols[0].text_input("할 일을 입력하세요")
    due_date = cols[1].date_input("마감일 선택", value=date.today())
    submit = cols[2].form_submit_button("추가")

if submit:
    if task_input.strip() != "":
        st.session_state.tasks.append({'task': task_input.strip(), 'due': due_date})

# 할 일 목록 출력
today = date.today()
for idx, item in enumerate(st.session_state.tasks):
    task = item['task']
    due = item['due']
    days_left = (due - today).days

    if days_left < 0:
        due_class = "due-past"
    elif days_left <= 3:
        due_class = "due-soon"
    else:
        due_class = "due-normal"

    # 삭제 버튼
    col1, col2, col3 = st.columns([8, 2, 1])
    with col1:
        st.markdown(
            f'<div class="task-text">• {task}</div>', unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="due-date {due_class}">📅 {due.strftime("%Y-%m-%d")}</div>', unsafe_allow_html=True
        )
    with col3:
        if st.button("❌", key=f"del_{idx}", help="할 일 삭제"):
            st.session_state.tasks.pop(idx)
            st.experimental_rerun()

# --- 타이머 기능 ---
st.markdown('<div class="timer-container">', unsafe_allow_html=True)

st.markdown('<h3>⏱️ 집중 타이머</h3>', unsafe_allow_html=True)

# 타이머 유형 선택
timer_type = st.selectbox("타이머 유형 선택", options=["집중 25분", "휴식 5분", "휴식 10분"], index=0, key="timer_type_select")

timer_seconds_map = {
    "집중 25분": 25 * 60,
    "휴식 5분": 5 * 60,
    "휴식 10분": 10 * 60,
}

# 타이머 초기화, 시작, 중지 함수
def start_timer():
    st.session_state.timer_seconds = timer_seconds_map[timer_type]
    st.session_state.timer_end_time = datetime.now() + timedelta(seconds=st.session_state.timer_seconds)
    st.session_state.timer_running = True

def stop_timer():
    st.session_state.timer_running = False
    st.session_state.timer_end_time = None
    st.session_state.timer_seconds = 0

# 타이머 버튼 UI
col_start, col_stop = st.columns(2)
with col_start:
    if st.button("시작", disabled=st.session_state.timer_running):
        start_timer()
with col_stop:
    if st.button("중지", disabled=not st.session_state.timer_running):
        stop_timer()

# 타이머 시간 계산 및 표시
if st.session_state.timer_running and st.session_state.timer_end_time:
    remaining = (st.session_state.timer_end_time - datetime.now()).total_seconds()
    if remaining <= 0:
        st.session_state.timer_running = False
        st.session_state.timer_seconds = 0
        st.session_state.timer_end_time = None
        st.success("⏰ 타이머 종료! 휴식을 취하세요.")
        remaining = 0
else:
    remaining = st.session_state.timer_seconds

mins = int(remaining // 60)
secs = int(remaining % 60)
timer_display = f"{mins:02d}:{secs:02d}"

st.markdown(f'<div class="timer-display">{timer_display}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 타이머 자동 갱신 (최대 1초 간격)
if st.session_state.timer_running:
    st.experimental_rerun()

