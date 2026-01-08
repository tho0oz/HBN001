import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 강력한 레이아웃 초기화 및 정렬 CSS
st.markdown("""
<style>
    /* [핵심] 스트림릿 내부의 모든 기본 여백과 최대 너비 제한 해제 */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stAppViewBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
        margin: 0 !important;
    }
    .stApp { background-color: #F2F5F8 !important; }

    /* [공통 규격] 헤더와 본문에 똑같이 적용할 가로 여백 (60px) */
    :root {
        --side-padding: 60px;
        --grid-gap: 20px;
    }

    /* [상단 고정 영역] */
    .sticky-top-area {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        background-color: rgba(242, 245, 248, 0.9);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 30px var(--side-padding) 20px var(--side-padding);
        box-sizing: border-box;
    }

    .main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.2px; }
    .sub-title { color: #6A7683; margin: 5px 0 25px 0; font-weight: 500; font-size: 0.85rem; }

    /* [그리드 레이아웃] 헤더와 본문 공통 */
    .roadmap-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: var(--grid-gap);
        width: 100%;
        box-sizing: border-box;
    }

    .month-label { 
        background-color: #FFFFFF; 
        color: #1A1A1A; 
        padding: 12px; 
        border-radius: 12px; 
        font-weight: 800; 
        font-size: 0.95rem; 
        text-align: center; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    }

    /* [본문 영역] 헤더 높이만큼 띄우고 첫 카드 위치 최적화 */
    .main-content-area {
        padding: 175px var(--side-padding) 60px var(--side-padding);
        width: 100%;
        box-sizing: border-box;
    }

    /* [카드 디자인] */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 20px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 12px; 
        overflow: hidden;
        transition: transform 0.2s ease;
    }
    .project-card:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.06); }

    summary { list-style: none; padding: 16px 20px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
    summary::-webkit-details-marker { display: none; }
    
    .card-project-title { font-size: 1.05rem; font-weight: 800; line-height: 1.2; color: #1A1A1A; }
    .card-content { padding: 0 20px 20px 20px; }
    .card-desc { font-size: 0.85rem; line-height: 1.5; margin: 8px 0; color: #333; font-weight: 500; }
    .card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.6; margin: 0; }

    .arrow-icon { width: 8px; height: 8px; border-top: 2.5px solid #BCB8AD; border-right: 2.5px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }

    .badge-wrapper { display: flex; gap: 4px; margin-top: 6px; }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 및 설정
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

# 4. 상단 고정 영역 렌더링
header_html = f"""
<div class="sticky-top-area">
    <div class="main-title">한빛앤 프로덕트 로드맵</div>
    <div class="sub-title">2026 상반기 마일스톤 타임라인</div>
    <div class="roadmap-grid">
        <div class="month-label">1월</div><div class="month-label">2월</div>
        <div class="month-label">3월</div><div class="month-label">4월</div>
        <div class="month-label">5월</div><div class="month-label">6월</div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 5. 메인 본문 영역 렌더링
if not df.empty:
    cards_html = '<div class="main-content-area"><div class="roadmap-grid" style="align-items: start;">'
    
    for _, row in df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            
            # 카드가 시작 월부터 종료 월까지 걸치도록 그리드 컬럼 설정
            grid_pos = f"grid-column: {start} / span {span};"
            
            cards_html += (
                f'<details class="project-card" style="{grid_pos}">'
                f'<summary><div>'
                f'<div class="card-project-title">{row["Project"]}</div>'
                f'<div class="badge-wrapper"><div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1.5px solid {theme["main"]}30;">{combined_label}</div></div>'
                f'</div><div class="arrow-icon"></div></summary>'
                f'<div class="card-content">'
                f'<div class="card-desc">{row["Description"]}</div>'
                f'<div class="card-manager">{row["Manager"]}</div>'
                f'</div></details>'
            )
        except: continue
        
    cards_html += '</div></div>'
    st.markdown(cards_html, unsafe_allow_html=True)
else:
    st.markdown('<div class="main-content-area">데이터 로딩 중...</div>', unsafe_allow_html=True)
