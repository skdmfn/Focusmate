import streamlit as st

st.set_page_config(page_title="Focusmate", page_icon="🎯", layout="centered")

# CSS 스타일 정의
st.markdown("""
<style>
/* 배경과 기본 폰트 */
body {
    background-color: #f4f7fa;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 카드 스타일 */
.card {
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* 헤더 */
h1, h2 {
    color: #2c3e50;
    font-weight: 700;
}

/* 버튼 커스텀 */
.stButton>button {
    background-color: #2e86de;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #1b4f72;
}

/* 텍스트 입력창 커스텀 */
div.stTextInput>div>input {
    border-radius: 8px;
    border: 1.5px solid #ccc;
    padding: 10px;
    font-size: 16px;
}

/* 할 일 목록 */
.todo-item {
    font-size: 18px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎯 Focusmate - 집중 생산성 앱")

# 투두 리스트 카드
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("✅ 할 일 목록")

task_input = st.text_input("새 작업 추가", key="task_input")

if st.button("추가"):
    if task_input.strip() != "":
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        st.session_state.tasks.append(task_input.strip())
        st.session_state.task_input = ""

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

for i, task in enumerate(st.session_state.tasks):
    cols = st.columns([9, 1])
    cols[0].markdown(f'<div class="todo-item">• {task}</div>', unsafe_allow_html=True)
    if cols[1].button("❌", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 타이머 카드
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("⏲️ 집중 타이머")
timer_length = st.slider("타이머 설정 (분)", 1, 60, 25)

st.markdown(f"""
<div style="text-align:center; font-size: 72px; font-weight: 700; color:#2e86de; margin-top: 20px;">
{timer_length:02}:00
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top: 20px;">
<button style="
    background-color:#2e86de; 
    color:white; 
    border:none; 
    padding: 12px 40px; 
    font-size: 20px; 
    border-radius: 10px;
    cursor:pointer;">
시작하기
</button>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
