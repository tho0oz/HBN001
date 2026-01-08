import streamlit as st
import pandas as pd
1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")
구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA'
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'
2. 디자인 CSS (상하 여백 긴급 축소)
st.markdown("""
<style>
    /* [1] 스트림릿 내부 반응형 패딩 및 마진 완전 박멸 */
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    /* 모든 캐시 컨테이너 및 블록 패딩 강제 0 */
    [data-testid="stAppViewBlockContainer"], 
    [data-testid="stVerticalBlock"],
    [class*="st-emotion-cache"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp { background-color: #F2F5F8 !important; }

    /* [2] 고정 규격 설정 */
    :root {
        --side-margin: 60px;
        --grid-column-gap: 20px; /* 가로 간격 */
        --grid-row-gap: 8px;     /* 세로 간격 (이 값을 줄여서 촘촘하게 만듭니다) */
    }

    /* 상단 고정 영역 */
    .sticky-top-area {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background-color: rgba(242, 245, 248, 0.9);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 30px var(--side-margin) 15px var(--side-margin);
        box-sizing: border-box;
    }

    .main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.2px; }
    .sub-title { color: #6A7683; margin: 5px 0 20px 0; font-weight: 500; font-size: 0.85rem; }

    /* 그리드 레이아웃 (세로 간격 row-gap 적용) */
    .roadmap-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        column-gap: var(--grid-column-gap);
        row-gap: var(--grid-row-gap); /* 카드 사이 상하 여백 조절 */
        width: 100%;
        box-sizing: border-box;
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

    /* [3] 본문 영역 */
    .main-content-area {
        margin-top: 155px; /* 헤더 높이 밀착 */
        padding: 0 var(--side-margin) 60px var(--side-margin);
        width: 100%;
        box-sizing: border-box;
    }

    /* 카드 디자인 (마진 제거 후 그리드 갭으로 제어) */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 20px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 0 !important; /* 상하 마진 제거 */
        overflow: hidden;
    }
    .project-card:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

    summary { list-style: none; padding: 14px 18px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
    summary::-webkit-details-marker { display: none; }
    
    .card-project-title { font-size: 1rem; font-weight: 800; color: #1A1A1A; }
    .card-content { padding: 0 18px 18px 18px; }
    .card-desc { font-size: 0.85rem; line-height: 1.4; margin: 6px 0; color: #333; font-weight: 500; }
    .card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.6; margin: 0; }

    .arrow-icon { width: 8px; height: 8px; border-top: 2px solid #BCB8AD; border-right: 2px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }

    .badge-wrapper { display: flex; gap: 4px; margin-top: 4px; }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)
3. 데이터 로드
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
4. 상단 고정 영역
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
5. 메인 본문 영역
if not df.empty:
cards_html = '<div class="main-content-area"><div class="roadmap-grid">'
for _, row in df.iterrows():
try:
start, end = int(row['StartMonth']), int(row['EndMonth'])
span = end - start + 1
cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
combined_label = f"{cat_name} {status_text}"
grid_pos = f"grid-column: {start} / span {span};"
code
Code
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
