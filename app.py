import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 파스텔 톤앤매너 CSS
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

    /* 프로젝트 카드 */
    .project-card {
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        transition: transform 0.2s ease;
    }
    .project-card:hover { transform: translateY(-3px); }

    .card-project-title { font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; }
    .card-desc { font-size: 0.9rem; line-height: 1.5; margin-bottom: 18px; opacity: 0.8; font-weight: 500; }
    .card-manager { font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; margin-bottom: 18px; }
    
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

# 새 카테고리 기준 색상 팔레트
COLOR_PALETTE = {
    "논의": {"bg": "#F1F3F5", "main": "#495057"},   # 차분한 그레이
    "기획": {"bg": "#FFF5F0", "main": "#FF9500"},   # 화사한 오렌지
    "디자인": {"bg": "#F5F0FF", "main": "#5E5CE6"}, # 세련된 퍼플
    "개발": {"bg": "#F0F7FF", "main": "#007AFF"},   # 시원한 블루
    "QA": {"bg": "#F0F9F0", "main": "#34C759"},    # 산뜻한 그린
    "배포": {"bg": "#FFF0F5", "main": "#FF2D55"},   # 강렬한 핑크
    "Default": {"bg": "#F8F9FA", "main": "#ADB5BD"}
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
                    # 카테고리에 맞는 색상 테마 선택
                    cat_name = str(row['Category']).strip()
                    theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
                    
                    st.markdown(f"""
                        <div class="project-card" style="background-color: {theme['bg']};">
                            <div class="card-project-title" style="color: #1A1A1A;">{row['Project']}</div>
                            <div class="card-desc" style="color: {theme['main']};">{row['Description']}</div>
                            <div class="card-manager" style="color: #4A4A4A;">
                                <span style="background: {theme['main']}; color: white; width: 22px; height: 22px; border-radius: 6px; display: inline-block; margin-right: 8px; text-align: center; line-height: 22px; font-size: 10px;">👤</span>
                                {row['Manager']}
                            </div>
                            <div class="badge-wrapper">
                                <div class="badge" style="background-color: white; color: {theme['main']}; border: 1.5px solid {theme['main']}20;">{row['Quarter']}</div>
                                <div class="badge" style="background-color: {theme['main']}; color: white;">{row['Status']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#AAB4BE; font-size:0.85rem; text-align:center; margin-top:10px;'>-</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
