import streamlit as st
import time

st.set_page_config(page_title="Focusmate", layout="centered")

st.title("📌 Focusmate")
st.subheader("할 일 목록과 집중 타이머를 함께 관리해보세요!")

# 할 일 관리
st.markdown("### ✅ 할 일 목록")
todo = st.text_input("할 일을 입력하세요")
if 'todos' not in st.session_state:
    st.session_state.todos = []

if st.button("추가"):
    if todo:
        st.session_state.todos.append({"task": todo, "done": False})

for i, item in enumerate(st.session_state.todos):
    st.session_state.todos[i]["done"] = st.checkbox(item["task"], value=item["done"])

# 타이머
st.markdown("### ⏲️ 집중 타이머")
minutes = st.slider("시간 설정 (분)", 1, 60, 25)
if st.button("타이머 시작"):
    for i in range(minutes * 60, 0, -1):
        st.markdown(f"⏳ 남은 시간: `{i // 60}:{i % 60:02}`")
        time.sleep(1)
    st.success("⏰ 집중 시간이 끝났습니다!")
