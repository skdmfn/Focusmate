import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(page_title="Focusmate - 집중 생산성 앱", page_icon="🎯", layout="centered")

# CSS 스타일 정의
st.markdown("""
<style>
.app-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #0B3D91;
    text-align: center;
    margin-bottom: 30px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.task-item {
    background-color: #E9F1F7;
    padding: 12px 15px;
    border-radius: 8px;
    margin-bottom: 10px;
    font-size: 1.1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 5px rgba(11, 61, 145, 0.15);
}
.task-text {
    flex-grow: 1;
    margin-right: 15px;
}
.due-date {
    font-size: 0.9rem;
    color: #555;
    min-width: 110px;
    text-align: right;
    white-space: nowrap;
}
.timer-container {
    background-color: #D6E6F2;
    padding: 20px 25px;
    border-radius: 12px;
    margin-top: 35px;
    box-shadow: 0 3px 8px rgba(11, 61, 145, 0.2);
}
.timer-display {
    font-size: 3rem;
    font-weight: 700;
    color: #0B3D91;
    text-align: center;
    margin-top: 15px;
    font-family: 'Courier New', Courier, monospace;
}
button {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

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

# 할 일 입력 폼
with st.form(key='task_form'):
    cols = st.columns([4, 2, 1])
    task_input = cols[0].text_input("할 일을 입력하세요")
    due_date = cols[1].date_input("마감일 선택", value=date.today())
    submit = cols[2].form_submit_button("추가")

if submit:
    if task_input.strip() != "":
        st.session_state.tasks.append({'task': task_input.strip(), 'due': due_date})

# 할 일 목록 출력
if st.session_state.tasks:
    st.markdown("### 📝 할 일 목록")
    for idx, item in enumerate(st.session_state.tasks):
        due_str = item['due'].strftime("%Y-%m-%d")
        task_html = f"""
        <div class="task-item">
            <div class="task-text">{item['task']}</div>
            <div class="due-date">{due_str}</div>
        </div>
        """
        st.markdown(task_html, unsafe_allow_html=True)
else:
    st.info("할 일을 추가해 주세요.")

# 타이머 영역 시작
st.markdown('<div class="timer-container">', unsafe_allow_html=True)
st.markdown('<h3>⏱️ 집중 타이머</h3>', unsafe_allow_html=True)

timer_type = st.selectbox(
    "타이머 유형 선택", 
    options=["집중 25분", "집중 50분", "휴식 5분", "휴식 10분"], 
    index=0,
    key="timer_type_select"
)

timer_seconds_map = {
    "집중 25분": 25 * 60,
    "집중 50분": 50 * 60,
    "휴식 5분": 5 * 60,
    "휴식 10분": 10 * 60,
}

def start_timer():
    st.session_state.timer_seconds = timer_seconds_map[timer_type]
    st.session_state.timer_end_time = datetime.now() + timedelta(seconds=st.session_state.timer_seconds)
    st.session_state.timer_running = True

def stop_timer():
    st.session_state.timer_running = False
    st.session_state.timer_end_time = None
    st.session_state.timer_seconds = 0

col_start, col_stop = st.columns(2)
with col_start:
    if st.button("시작", disabled=st.session_state.timer_running):
        start_timer()
with col_stop:
    if st.button("중지", disabled=not st.session_state.timer_running):
        stop_timer()

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

# 타이머 실행 중이면 페이지 자동 갱신
if st.session_state.timer_running:
    st.experimental_rerun()


# 타이머 자동 갱신 (최대 1초 간격)
if st.session_state.timer_running:
    st.experimental_rerun()

