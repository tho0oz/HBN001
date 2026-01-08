import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS
st.markdown("""
<style>
    /* Streamlit 기본 UI 숨기기 */
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    
    /* 전체 배경 및 여백 최적화 */
    .stApp { background-color: #F2F5F8; }
    .main .block-container { 
        padding-top: 1.5rem !important; /* 상단 여백 대폭 축소 */
        padding-bottom: 0rem !important;
    }

    /* 제목 영역 */
    .main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; padding: 0; letter-spacing: -1.2px; }
    .sub-title { color: #6A7683; margin-bottom: 20px; font-weight: 500; font-size: 0.8rem; }

    /* 타임라인 그리드 컨테이너 */
    .roadmap-container { 
        display: grid; 
        grid-template-columns: repeat(6, 1fr); 
        gap: 12px; 
        align-items: start;
        position: relative;
    }

    /* 월 헤더 고정 및 그라데이션 영역 */
    .month-label { 
        background-color: #FFFFFF; 
        color: #1A1A1A; 
        padding: 8px; 
        border-radius: 12px; 
        font-weight: 800; 
        font-size: 0.9rem; 
        text-align: center; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
        
        /* 고정 위치 및 상하 여백 */
        position: sticky; 
        top: 15px;      /* 상단 여백 */
        margin-bottom: 15px; /* 하단 여백 */
        z-index: 999;
    }

    /* 헤더 뒤쪽 그라데이션 페이드 효과 */
    .roadmap-container::before {
        content: "";
        position: sticky;
        top: 0;
        grid-column: 1 / span 6;
        height: 60px; /* 그라데이션 높이 */
        background: linear-gradient(to bottom, #F2F5F8 60%, rgba(242,245,248,0) 100%);
        z-index: 998;
        margin-bottom: -60px; /* 레이아웃 영향 방지 */
        pointer-events: none;
    }

    /* 카드 디자인 (흰색 박스, 촘촘한 간격) */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 18px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 6px; 
        overflow: hidden;
        transition: all 0.2s ease;
    }
    .project-card:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.06); }

    summary { list-style: none; padding: 12px 16px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
    summary::-webkit-details-marker { display: none; }
    
    /* 프로젝트 타이틀 (검정색 고정) */
    .card-project-title { font-size: 1rem; font-weight: 800; line-height: 1.2; color: #1A1A1A; }

    .card-content { padding: 0 16px 16px 16px; }
    .card-desc { font-size: 0.85rem; line-height: 1.4; margin: 6px 0; color: #333; font-weight: 500; }
    .card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.6; margin: 0; }

    .arrow-icon { width: 8px; height: 8px; border-top: 2px solid #BCB8AD; border-right: 2px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }

    .badge-wrapper { display: flex; gap: 4px; margin-top: 6px; }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 및 컬러 설정
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
    
    # 1월~6월 고정 헤더
    for i in range(1, 7):
        full_html += f'<div class="month-label" style="grid-column: {i};">{i}월</div>'

    # 카드 출력 (타이틀 검정색)
    for _, row in df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            grid_pos = f"grid-column: {start} / span {span};"
            
            card_html = (
                f'<details class="project-card" style="{grid_pos}">'
                f'<summary>'
                f'<div>'
                f'<div class="card-project-title">{row["Project"]}</div>'
                f'<div class="badge-wrapper"><div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1.5px solid {theme["main"]}30;">{combined_label}</div></div>'
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
