import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정 (사이드바 제거 및 레이아웃 확장)
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 이미지 감성을 담은 CSS (가로 정렬 및 한국어 텍스트 최적화)
st.markdown("""
    <style>
    /* 기본 설정 */
    [data-testid="stSidebar"] {display: none;}
    .stApp {background-color: #F9F7F2;}
    
    /* 제목 스타일 */
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1A1A1A; padding: 20px 0 10px 0; letter-spacing: -1.5px; }
    
    /* 가로 스크롤 컨테이너 */
    .horizontal-container {
        display: flex;
        overflow-x: auto;
        gap: 25px;
        padding: 20px 5px;
        scroll-behavior: smooth;
    }
    
    /* 각 월별 열(Column) 스타일 */
    .month-column {
        min-width: 320px;
        max-width: 320px;
    }

    /* 월 헤더 디자인 (이미지 포인트) */
    .month-header {
        background-color: #1A1A1A;
        color: white;
        padding: 10px 20px;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        margin-bottom: 25px;
    }

    /* 프로젝트 카드 디자인 */
    .project-card {
        background-color: #FFFFFF;
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.02);
    }

    .card-project-title { font-size: 1.2rem; font-weight: 800; color: #1A1A1A; margin-bottom: 8px; }
    .card-desc { font-size: 0.9rem; color: #6F6F6F; line-height: 1.5; margin-bottom: 18px; height: 2.8em; overflow: hidden; }
    .card-manager { font-size: 0.85rem; font-weight: 600; color: #333; display: flex; align-items: center; margin-bottom: 18px; }
    
    /* 뱃지 디자인 */
    .badge-wrapper { display: flex; gap: 8px; }
    .badge-q { 
        background-color: #1A1A1A; color: white; border-radius: 10px; 
        padding: 5px 12px; font-size: 0.7rem; font-weight: 700; 
    }
    .badge-status { 
        background-color: #F0F0F0; color: #1A1A1A; border-radius: 10px; 
        padding: 5px 12px; font-size: 0.7rem; font-weight: 700; border: 1px solid #E0E0E0;
    }
    
    /* 스크롤바 커스텀 */
    .horizontal-container::-webkit-scrollbar { height: 8px; }
    .horizontal-container::-webkit-scrollbar-track { background: #EBE7DE; border-radius: 10px; }
    .horizontal-container::-webkit-scrollbar-thumb { background: #BCB8AD; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

ACCENT_COLORS = {
    "Design": "#FFD1ED", "Dev": "#D1E4FF", "Planning": "#FFEFD1", "Meeting": "#D1FFDE", "Urgent": "#E5D1FF"
}

try:
    df = load_data()
    
    # 상단 헤더 (수정된 텍스트)
    st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#888; margin-bottom:40px;">2026 상반기 주요 마일스톤</p>', unsafe_allow_html=True)

    # 가로 스크롤 레이아웃 시작
    # Streamlit 안에서 HTML 태그를 직접 닫을 수 없으므로, 컬럼 기능을 조합하여 구성합니다.
    cols = st.columns(6) # 1월부터 6월까지 6개 컬럼 생성
    
    month_names = ["1월", "2월", "3월", "4월", "5월", "6월"]
    
    for i, m_name in enumerate(month_names, 1):
        with cols[i-1]:
            st.markdown(f'<div class="month-header">{m_name}</div>', unsafe_allow_html=True)
            
            # 해당 월 데이터 필터링
            month_data = df[df['Date'].dt.month == i]
            
            if len(month_data) > 0:
                for _, row in month_data.iterrows():
                    bg_color = ACCENT_COLORS.get(row['Category'], "#FFFFFF")
                    
                    st.markdown(f"""
                        <div class="project-card">
                            <div class="card-project-title">{row['Project']}</div>
                            <div class="card-desc">{row['Description']}</div>
                            <div class="card-manager">
                                <span style="background:{bg_color}; width:24px; height:24px; border-radius:50%; display:inline-block; margin-right:8px; text-align:center; line-height:24px; font-size:10px;">👤</span>
                                {row['Manager']}
                            </div>
                            <div class="badge-wrapper">
                                <div class="badge-q">{row['Quarter']}</div>
                                <div class="badge-status">{row['Status']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#BCB8AD; font-size:0.8rem; font-style:italic;'>예정된 프로젝트 없음</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
