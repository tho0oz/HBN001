import streamlit as st
import pandas as pd

st.set_page_config(page_title="협업 대시보드", layout="wide")

st.title("🚀 프로젝트 협업 대시보드")

# 데이터 설정 (이 부분을 수정해서 업무를 관리하세요)
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"업무": "기획서 작성", "담당자": "김철수", "진척도": 100, "상태": "완료"},
        {"업무": "디자인 작업", "담당자": "이영희", "진척도": 50, "상태": "진행중"},
        {"업무": "서버 구축", "담당자": "박지민", "진척도": 10, "상태": "대기"}
    ])

# 1. 로드맵 (진척도 시각화)
st.header("📍 전체 로드맵")
for index, row in st.session_state.tasks.iterrows():
    st.write(f"**{row['업무']}** ({row['담당자']})")
    st.progress(row['진척도'] / 100)

# 2. 상세 업무 리스트
st.header("📝 업무 상세 현황")
st.table(st.session_state.tasks)

# 3. 새로운 업무 추가 기능
st.sidebar.header("➕ 새 업무 추가")
new_task = st.sidebar.text_input("업무명")
new_owner = st.sidebar.text_input("담당자")
new_progress = st.sidebar.slider("진척도", 0, 100, 0)

if st.sidebar.button("추가하기"):
    new_data = {"업무": new_task, "담당자": new_owner, "진척도": new_progress, "상태": "진행중"}
    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_data])], ignore_index=True)
    st.rerun()
