import streamlit as st
from datetime import date

# 페이지 설정
st.set_page_config(page_title="Focusmate - 집중 생산성 앱", page_icon="🎯", layout="centered")

# CSS 스타일 (모던하고 깔끔한 느낌)
st.markdown(
    """
    <style>
    .app-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #4B6EAF;
        margin-bottom: 1rem;
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
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-header">🎯 Focusmate - 집중 생산성 앱</div>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# 할 일 입력 및 날짜 선택 UI
with st.form(key='task_form'):
    cols = st.columns([4, 2, 1])
    task_input = cols[0].text_input("할 일을 입력하세요")
    due_date = cols[1].date_input("마감일 선택", value=date.today())
    submit = cols[2].form_submit_button("추가")

if submit:
    if task_input.strip() != "":
        st.session_state.tasks.append({'task': task_input.strip(), 'due': due_date})

# 오늘 날짜
today = date.today()

# 할 일 목록 출력
for idx, item in enumerate(st.session_state.tasks):
    task = item['task']
    due = item['due']
    days_left = (due - today).days

    # 마감일 상태에 따른 클래스 지정
    if days_left < 0:
        due_class = "due-past"
    elif days_left <= 3:
        due_class = "due-soon"
    else:
        due_class = "due-normal"

    st.markdown(
        f"""
        <div class="task-item">
            <div class="task-text">• {task}</div>
            <div class="due-date {due_class}">📅 {due.strftime('%Y-%m-%d')}</div>
            <div class="delete-btn" onclick="delete_task({idx})" id="del_{idx}">❌</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 삭제 버튼 기능 처리
for idx in range(len(st.session_state.tasks)):
    if st.button(f"delete_{idx}", key=f"del_btn_{idx}"):
        st.session_state.tasks.pop(idx)
        st.experimental_rerun()

