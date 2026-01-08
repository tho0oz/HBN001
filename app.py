import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (고정 기능 해결 및 간격 축소)
st.markdown("""
<style>
    /* 기본 배경 및 사이드바 제거 */
    [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #F2F5F8; }
    
    /* 제목 영역 간격 축소 */
    .main-title { font-size: 2rem; font-weight: 800; color: #1A1A1A; padding: 10px 0 0 0; letter-spacing: -1.2px; }
    .sub-title { color: #6A7683; margin-bottom: 25px; font-weight: 500; font-size: 0.85rem; }

    /* 타임라인 그리드: 상하 간격 축소 */
    .roadmap-container { 
        display: grid; 
        grid-template-columns: repeat(6, 1fr); 
        gap: 12px; 
        align-items: start;
        overflow: visible; /* sticky 작동을 위해 필수 */
    }

    /* 월 헤더 고정 기능 해결 */
    .month-label { 
        background-color: #FFFFFF; 
        color: #1A1A1A; 
        padding: 8px; 
        border-radius: 12px; 
        font-weight: 800; 
        font-size: 0.9rem; 
        text-align: center; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
        margin-bottom: 10px;
        
        /* 고정 설정: 스트림릿 헤더 높이를 고려하여 top 값 조정 */
        position: sticky; 
        top: 45px;      
        z-index: 999;
    }

    /* 카드 디자인 최적화 (사이즈 축소, Radius 18px) */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 18px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 6px; /* 카드 간 상하 간격 촘촘하게 */
        overflow: hidden;
        transition: all 0.2s ease;
    }

    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.06);
    }

    /* 카드 내부 간격 축소 (Padding 24px -> 14px) */
    summary {
        list-style: none; 
        padding: 14px 16px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    summary::-webkit-details-marker { display: none; }

    .card-project-title { font-size: 1rem; font-weight: 800; line-height: 1.2; }

    /* 펼쳤을 때 텍스트 간격 좁게 조정 */
    .card-content { padding: 0 16px 16px 16px; }
    .card-desc { 
        font-size: 0.85rem; 
        line-height: 1.4; 
        margin: 8px 0; 
        color: #333; 
        font-weight: 500; 
    }
    .card-manager { 
        font-size: 0.75rem; 
        color: #1A1A1A; 
        opacity: 0.6; 
        margin: 0; 
    }

    /* 화살표 사이즈 축소 */
    .arrow-icon {
        width: 8px;
        height: 8px;
        border-top: 2px solid #BCB8AD;
        border-right: 2px solid #BCB8AD;
        transform: rotate(135deg);
        transition: transform 0.3s ease;
    }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }

    /* 뱃지 사이즈 축소 */
    .badge-wrapper { display: flex; gap: 4px; margin-top: 6px; }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드
COLOR_PALETTE = {
    "논의": {"main": "#495057"}, "기획": {"main": "#FF9500"}, "디자인": {"main": "#5E5CE6"},
    "개발": {"main": "#007AFF"}, "QA": {"main": "#34C759"}, "배포": {"main": "#FF2D55"},
    "Default": {"main": "#ADB5BD"}
}

@st.cache_data(ttl=5)
def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame()

df = load_data()

# 4. 화면 출력
st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 상반기 마일스톤 타임라인</div>', unsafe_allow_html=True)

if not df.empty:
    full_html = '<div class="roadmap-container">'
    
    # 월 헤더 (Sticky 고정 적용)
    for i in range(1, 7):
        full_html += f'<div class="month-label" style="grid-column: {i};">{i}월</div>'

    # 프로젝트 카드 출력
    for _, row in df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            grid_pos = f"grid-column: {start} / span {span};"
            
            # 촘촘한 간격의 카드 HTML
            card_html = (
                f'<details class="project-card" style="{grid_pos}">'
                f'<summary>'
                f'<div>'
                f'<div class="card-project-title" style="color: {theme["main"]};">{row["Project"]}</div>'
                f'<div class="badge-wrapper"><div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1px solid {theme["main"]}30;">{combined_label}</div></div>'
                f'</div>'
                f'<div class="arrow-icon"></div>'
                f'</summary>'
                f'<div class="card-content">'
                f'<div class="card-desc">{row["Description"]}</div>'
                f'<div class="card-manager">{row["Manager"]}</div>'
                f'</div>'
                f'</details>'
            )
            full_html += card_html
        except: continue

    full_html += '</div>'
    st.markdown(full_html, unsafe_allow_html=True)
