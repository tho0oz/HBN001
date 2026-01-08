import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정 (사이드바 제거 및 레이아웃 확장)
st.set_page_config(page_title="2026 Roadmap", layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# CSS: 사이드바 숨기기 및 알록달록 카드 디자인
st.markdown("""
    <style>
    /* 사이드바 완전히 제거 */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    .stApp {background-color: #FFFFFF;}
    
    /* 카드 디자인 */
    .project-card {
        background-color: #fcfcfc;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .title-text { font-size: 1.25rem; font-weight: 800; color: #111; margin-bottom: 5px; }
    .desc-text { font-size: 0.9rem; color: #666; margin-bottom: 15px; line-height: 1.4; }
    .manager-text { font-size: 0.85rem; font-weight: 600; color: #444; margin-bottom: 15px; display: flex; align-items: center; }
    
    /* 뱃지 스타일 */
    .badge-container { display: flex; gap: 8px; }
    .badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-q { background-color: #111; color: white; } /* 분기 뱃지 */
    .badge-status { background-color: #E0E0E0; color: #444; } /* 상태 뱃지 기본 */
    
    /* 월 헤더 */
    .month-header {
        font-size: 1.8rem;
        font-weight: 900;
        margin: 40px 0 20px 0;
        border-bottom: 3px solid #111;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 불러오기
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# 카테고리별 강조 색상 (카드 왼쪽 선 포인트)
CATEGORY_COLORS = {
    "Design": "#FF3DAB", "Dev": "#007AFF", "Planning": "#FFAB00", "Meeting": "#00C752", "Urgent": "#7000FF"
}

try:
    df = load_data()
    
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>2026 First Half Roadmap</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>January - June Project Overview</p>", unsafe_allow_html=True)

    # 1월부터 6월까지 반복
    months = ["January", "February", "March", "April", "May", "June"]
    
    for i, month_name in enumerate(months, 1):
        # 해당 월의 데이터 필터링
        month_data = df[df['Date'].dt.month == i]
        
        st.markdown(f"<div class='month-header'>{month_name.upper()}</div>", unsafe_allow_html=True)
        
        if len(month_data) > 0:
            # 한 줄에 3개씩 배치
            cols = st.columns(3)
            for idx, (_, row) in enumerate(month_data.iterrows()):
                with cols[idx % 3]:
                    color = CATEGORY_COLORS.get(row['Category'], "#111")
                    
                    # 카드 출력
                    st.markdown(f"""
                        <div class="project-card" style="border-top: 5px solid {color};">
                            <div class="title-text">{row['Project']}</div>
                            <div class="desc-text">{row['Description']}</div>
                            <div class="manager-text">👤 {row['Manager']}</div>
                            <div class="badge-container">
                                <span class="badge badge-q">{row['Quarter']}</span>
                                <span class="badge badge-status" style="background-color: {color}20; color: {color};">
                                    {row['Status']}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"{month_name}에는 예정된 프로젝트가 없습니다.")

except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
    st.info("구글 시트 헤더가 [Project, Description, Manager, Date, Quarter, Status, Category] 인지 확인하세요.")
