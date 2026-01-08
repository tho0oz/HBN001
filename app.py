import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 설정 및 디자인 (이미지 스타일 적용)
st.set_page_config(page_title="Team Dashboard", layout="wide")

# CSS: 이미지와 비슷한 느낌을 주기 위한 디자인 코드
st.markdown("""
    <style>
    /* 전체 배경색 */
    .main {
        background-color: #f8f9fa;
    }
    /* 카드 스타일 */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f0f0;
    }
    /* 카드 안의 글자 크기 */
    div[data-testid="stMetricValue"] {
        font-size: 40px !important;
        font-weight: 700 !important;
        color: #1d1d1f;
    }
    /* 버튼/탭 스타일 커스텀 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e0e0e0;
        border-radius: 10px;
        padding: 10px 20px;
        color: #555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: white !important;
    }
    /* 컨테이너 스타일 */
    .task-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 불러오기
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    return df

try:
    df = load_data()
    now = datetime.now()
    
    # 헤더 섹션
    st.markdown(f"### 🏢 {now.year} Project Dashboard")
    st.caption("실시간 업무 진척도 및 로드맵 관리")

    # 상단 요약 카드 (이미지의 92%, 87% 느낌)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    avg_progress = int(df['Progress'].mean())
    this_month = df[df['End'].dt.month == now.month]
    
    col_m1.metric("전체 진척도", f"{avg_progress}%")
    col_m2.metric("이번 달 업무", f"{len(this_month)}개")
    col_m3.metric("완료 업무", f"{len(df[df['Status']=='완료'])}개")
    col_m4.metric("진행 중", f"{len(df[df['Status']=='진행중'])}개")

    st.write("---")

    # 메인 레이아웃: 왼쪽(로드맵), 오른쪽(카드형 리스트)
    left_col, right_col = st.columns([1.5, 1])

    with left_col:
        st.markdown("#### 📅 1년 로드맵")
        fig = px.timeline(df, 
                         x_start="Start", x_end="End", y="Task", 
                         color="Status", 
                         template="plotly_white",
                         color_discrete_sequence=["#000000", "#7f7f7f", "#e0e0e0"]) # 무채색 톤
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=400,
            showlegend=False
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with right_col:
        st.markdown(f"#### 📌 {now.month}월 진행 현황")
        if len(this_month) > 0:
            for _, row in this_month.iterrows():
                # 이미지의 카드 스타일 재현
                st.markdown(f"""
                <div class="task-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; font-size: 18px;">{row['Task']}</span>
                        <span style="background: #f0f0f0; padding: 4px 10px; border-radius: 10px; font-size: 12px;">{row['Owner']}</span>
                    </div>
                    <div style="font-size: 32px; font-weight: 800; margin: 10px 0;">{row['Progress']}%</div>
                    <div style="background: #eee; height: 8px; border-radius: 5px;">
                        <div style="background: black; width: {row['Progress']}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("이번 달 예정된 업무가 없습니다.")

except Exception as e:
    st.error(f"구글 시트를 불러올 수 없습니다. 설정을 확인해주세요. ({e})")
