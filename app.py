import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 요청 사항이 반영된 CSS 디자인
st.markdown("""
    <style>
    /* 배경: 연한 블루빛 회색 */
    [data-testid="stSidebar"] {display: none;}
    .stApp {
        background-color: #F2F5F8; 
    }
    
    /* 제목 스타일 */
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1A1A1A; padding: 20px 0 5px 0; letter-spacing: -1.5px; }
    .sub-title { color: #6A7683; margin-bottom: 40px; font-weight: 500; }

    /* 월 헤더 */
    .month-header {
        background-color: #FFFFFF;
        color: #1A1A1A;
        padding: 12px 20px;
        border-radius: 15px;
        font-weight: 800;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }

    /* 프로젝트 카드: 배경 흰색으로 고정 */
    .project-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 15px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        transition: transform 0.2s ease;
    }
    .project-card:hover { transform: translateY(-3px); }

    /* 프로젝트 명 (카테고리 컬러 적용) */
    .card-project-title { font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; }
    
    /* 설명 (기존 타이틀 컬러인 검정색 적용) */
    .card-desc { font-size: 0.9rem; line-height: 1.5; margin-bottom: 18px; color: #1A1A1A; font-weight: 500; }
    
    /* 담당자: 폰트 줄임, Regular(400), 투명도 70% */
    .card-manager { font-size: 0.75rem; font-weight: 400; color: #1A1A1A; opacity: 0.7; margin-bottom: 18px; }
    
    /* 뱃지 디자인 */
    .badge-wrapper { display: flex; gap: 6px; }
    .badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# 카테고리별 컬러 팔레트 (텍스트 및 뱃지용)
COLOR_PALETTE = {
    "논의": {"main": "#495057"},   # 그레이
    "기획": {"main": "#FF9500"},   # 오렌지
    "디자인": {"main": "#5E5CE6"}, # 퍼플
    "개발": {"main": "#007AFF"},   # 블루
    "QA": {"main": "#34C759"},    # 그린
    "배포": {"main": "#FF2D55"},   # 핑크
    "Default": {"main": "#ADB5BD"}
}

try:
    df = load_data()
    
    st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">2026 상반기 마일스톤 (1월 - 6월)</div>', unsafe_allow_html=True)

    # 1월부터 6월까지 가로 배치
    cols = st.columns(6)
    month_names = ["1월", "2월", "3월", "4월", "5월", "6월"]
    
    for i, m_name in enumerate(month_names, 1):
        with cols[i-1]:
            st.markdown(f'<div class="month-header">{m_name}</div>', unsafe_allow_html=True)
            
            month_data = df[df['Date'].dt.month == i]
            
            if len(month_data) > 0:
                for _, row in month_data.iterrows():
                    cat_name = str(row['Category']).strip()
                    theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
                    
                    st.markdown(f"""
                        <div class="project-card">
                            <!-- 프로젝트 명에 카테고리 컬러 적용 -->
                            <div class="card-project-title" style="color: {theme['main']};">{row['Project']}</div>
                            <!-- 설명에 검정색 적용 -->
                            <div class="card-desc">{row['Description']}</div>
                            <!-- 담당자 수정: 아이콘 제거, 폰트 축소, 투명도 70% -->
                            <div class="card-manager">{row['Manager']}</div>
                            <div class="badge-wrapper">
                                <div class="badge" style="background-color: {theme['main']}15; color: {theme['main']}; border: 1.5px solid {theme['main']}20;">{row['Quarter']}</div>
                                <div class="badge" style="background-color: {theme['main']}; color: white;">{row['Status']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#AAB4BE; font-size:0.85rem; text-align:center; margin-top:10px;'>-</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
