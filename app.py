import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (정렬 일치 및 구분선 제거)
st.markdown("""
<style>
    /* Streamlit 기본 UI 숨기기 */
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    
    /* 전체 배경 */
    .stApp { background-color: #F2F5F8; }
    
    /* [수정] 상단 고정 영역: 구분선 제거 및 너비 최적화 */
    .sticky-top-area {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background-color: rgba(242, 245, 248, 0.85);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 2rem 5rem 1rem 5rem; /* 아래쪽 여백 조절 */
        border-bottom: none; /* 구분선 삭제 */
    }

    /* 제목 및 서브제목 */
    .main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; padding: 0; letter-spacing: -1.2px; line-height: 1.2; }
    .sub-title { color: #6A7683; margin-bottom: 20px; font-weight: 500; font-size: 0.85rem; }

    /* [수정] 월 헤더 그리드: 하단 로드맵 그리드와 완벽 일치 */
    .month-grid-header {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 16px; /* 하단 gap과 통일 */
        width: 100%;
    }

    .month-label { 
        background-color: #FFFFFF; 
        color: #1A1A1A; 
        padding: 10px; 
        border-radius: 12px; 
        font-weight: 800; 
        font-size: 0.9rem; 
        text-align: center; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    }

    /* [수정] 메인 콘텐츠 영역: 상단 여백 및 정렬 일치 */
    .main-content-area {
        margin-top: 190px; /* 고정 영역 높이에 맞춰 정밀 조정 */
        padding: 0 5rem;
        width: 100%;
    }

    .roadmap-container { 
        display: grid; 
        grid-template-columns: repeat(6, 1fr); 
        gap: 16px; /* 상단 gap과 통일 */
        align-items: start;
        width: 100%;
    }

    /* 카드 디자인 */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 18px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 12px; 
        overflow: hidden;
        transition: all 0.2s ease;
    }
    .project-card:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.06); }

    summary { list-style: none; padding: 14px 18px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
    summary::-webkit-details-marker { display: none; }
    
    .card-project-title { font-size: 1.05rem; font-weight: 800; line-height: 1.2; color: #1A1A1A; }
    .card-content { padding: 0 18px 18px 18px; }
    .card-desc { font-size: 0.85rem; line-height: 1.5; margin: 8px 0; color: #333; font-weight: 500; }
    .card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.6; margin: 0; }

    .arrow-icon { width: 8px; height: 8px; border-top: 2px solid #BCB8AD; border-right: 2px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }

    .badge-wrapper { display: flex; gap: 4px; margin-top: 6px; }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; }

    /* 반응형 여백 (화면 너비에 따른 최적화) */
    @media (max-width: 1200px) {
        .sticky-top-area, .main-content-area { padding-left: 2rem; padding-right: 2rem; }
    }
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

# 4. 상단 고정 영역 (구분선 제거 및 월 레이블 출력)
header_html = f"""
<div class="sticky-top-area">
    <div class="main-title">한빛앤 프로덕트 로드맵</div>
    <div class="sub-title">2026 상반기 마일스톤 타임라인</div>
    <div class="month-grid-header">
        <div class="month-label">1월</div>
        <div class="month-label">2월</div>
        <div class="month-label">3월</div>
        <div class="month-label">4월</div>
        <div class="month-label">5월</div>
        <div class="month-label">6월</div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 5. 메인 콘텐츠 영역 (프로젝트 카드)
if not df.empty:
    # 촘촘한 정렬을 위해 동일한 grid 구조 사용
    cards_html = '<div class="main-content-area"><div class="roadmap-container">'
    
    for _, row in df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            
            # CSS Grid column 설정: 월 헤더와 동일한 위치로 고정
            grid_pos = f"grid-column: {start} / span {span};"
            
            cards_html += (
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
        except: continue
        
    cards_html += '</div></div>'
    st.markdown(cards_html, unsafe_allow_html=True)
