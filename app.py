import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정 (사이드바 제거 및 레이아웃 확장)
st.set_page_config(page_title="2026 Strategy Roadmap", layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 이미지의 감성을 담은 CSS 디자인
st.markdown("""
    <style>
    /* 배경 및 사이드바 제거 */
    [data-testid="stSidebar"] {display: none;}
    .stApp {background-color: #F9F7F2;} /* 이미지 특유의 크림색 배경 */
    
    /* 상단 헤더 영역 */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0 40px 0;
    }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1A1A1A; letter-spacing: -1px; }
    
    /* 월별 섹션 타이틀 */
    .month-section {
        background-color: #EBE7DE;
        padding: 8px 20px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.9rem;
        color: #444;
        display: inline-block;
        margin: 30px 0 15px 0;
    }

    /* 이미지 스타일의 프로젝트 카드 */
    .project-card {
        background-color: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.02);
        transition: all 0.3s ease;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }

    .card-project-title { font-size: 1.3rem; font-weight: 800; color: #1A1A1A; margin-bottom: 8px; }
    .card-desc { font-size: 0.95rem; color: #6F6F6F; line-height: 1.5; margin-bottom: 20px; }
    .card-manager { font-size: 0.85rem; font-weight: 600; color: #333; display: flex; align-items: center; margin-bottom: 20px; }
    
    /* 뱃지 디자인 (이미지 참고) */
    .badge-wrapper { display: flex; gap: 10px; }
    .badge-q { 
        background-color: #1A1A1A; color: white; border-radius: 12px; 
        padding: 6px 14px; font-size: 0.75rem; font-weight: 700; 
    }
    .badge-status { 
        background-color: #F0F0F0; color: #1A1A1A; border-radius: 12px; 
        padding: 6px 14px; font-size: 0.75rem; font-weight: 700; border: 1px solid #E0E0E0;
    }
    
    /* 장식용 가로선 */
    .dotted-line { border-top: 2px dashed #E0DCD0; margin: 10px 0 25px 0; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# 카테고리별 컬러 (카드 포인트용)
ACCENT_COLORS = {
    "Design": "#FFD1ED", "Dev": "#D1E4FF", "Planning": "#FFEFD1", "Meeting": "#D1FFDE", "Urgent": "#E5D1FF"
}

try:
    df = load_data()
    
    # 상단 헤더
    st.markdown("""
        <div class="header-container">
            <div class="main-title">Stay up to date, 2026 Roadmap</div>
            <div style="font-size: 1.5rem;">🔍 👤 ⚙️</div>
        </div>
    """, unsafe_allow_html=True)

    # 1월부터 6월까지 출력
    months = ["January", "February", "March", "April", "May", "June"]
    
    for i, month_name in enumerate(months, 1):
        month_data = df[df['Date'].dt.month == i]
        
        st.markdown(f'<div class="month-section">{month_name.upper()} 2026</div>', unsafe_allow_html=True)
        st.markdown('<div class="dotted-line"></div>', unsafe_allow_html=True)
        
        if len(month_data) > 0:
            cols = st.columns(3) # 한 줄에 3개 카드 배치
            for idx, (_, row) in enumerate(month_data.iterrows()):
                with cols[idx % 3]:
                    # 카테고리별 배경색 결정
                    bg_color = ACCENT_COLORS.get(row['Category'], "#FFFFFF")
                    
                    st.markdown(f"""
                        <div class="project-card">
                            <div class="card-project-title">{row['Project']}</div>
                            <div class="card-desc">{row['Description']}</div>
                            <div class="card-manager">
                                <span style="background:{bg_color}; width:30px; height:30px; border-radius:50%; display:inline-block; margin-right:10px; text-align:center; line-height:30px;">👤</span>
                                {row['Manager']}
                            </div>
                            <div class="badge-wrapper">
                                <div class="badge-q">{row['Quarter']}</div>
                                <div class="badge-status">{row['Status']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#A09E97; font-style:italic;'>No projects scheduled for this month.</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"오류 발생: {e}")
    st.info("시트 컬럼: Project, Description, Manager, Date, Quarter, Status, Category")
