import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 환경 설정 및 구글 시트 연동
# 여기에 복사한 구글 시트 ID를 입력하세요
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

st.set_page_config(page_title="Project Dashboard", layout="wide")

# 데이터 불러오기 함수
@st.cache_data(ttl=60) # 60초마다 데이터 갱신
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    return df

try:
    df = load_data()

    # 상단 타이틀 및 이번 달 요약
    st.title("📊 프로젝트 협업 통합 대시보드")
    
    # 요약 지표 (Metrics)
    now = datetime.now()
    this_month_tasks = df[df['End'].dt.month == now.month]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 프로젝트", f"{len(df)}건")
    col2.metric("이번 달 종료 예정", f"{len(this_month_tasks)}건")
    col3.metric("평균 진척도", f"{int(df['Progress'].mean())}%")

    # 탭 메뉴 구성
    tab1, tab2 = st.tabs(["📅 1년 로드맵 (Gantt Chart)", "📌 이번 달 상세 현황"])

    with tab1:
        st.subheader("연간 업무 로드맵")
        # 로드맵 차트 (간트 차트) 생성
        fig = px.timeline(df, 
                         x_start="Start", 
                         x_end="End", 
                         y="Task", 
                         color="Status",
                         hover_data=['Owner', 'Progress'],
                         color_discrete_map={'완료': '#26a69a', '진행중': '#29b6f6', '대기': '#ef5350'})
        
        fig.update_yaxes(autorange="reversed") # 최신 항목이 위로
        fig.update_layout(height=500, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(f"📅 {now.month}월 진행 사항")
        if len(this_month_tasks) > 0:
            for _, row in this_month_tasks.iterrows():
                with st.container():
                    c1, c2, c3 = st.columns([2, 1, 3])
                    c1.write(f"**{row['Task']}**")
                    c2.write(f"👤 {row['Owner']}")
                    c3.progress(int(row['Progress']))
        else:
            st.info("이번 달에 예정된 업무가 없습니다.")
        
        st.divider()
        st.subheader("📋 전체 데이터 표")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("구글 시트 연결에 실패했습니다. ID가 정확한지, 공유 설정이 '링크가 있는 모든 사용자'인지 확인해주세요.")
    st.info(f"에러 내용: {e}")

st.sidebar.markdown("### 💡 관리 팁")
st.sidebar.info("구글 스프레드시트에서 데이터를 수정하고 1분 뒤 새로고침하면 웹사이트에 반영됩니다.")
