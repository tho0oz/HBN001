import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (필터 고정 및 여백 밀착)
st.markdown("""
<style>
    /* 스트림릿 기본 UI 제거 */
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
    [class*="st-emotion-cache"] { padding-top: 0 !important; }
    .stApp { background-color: #F2F5F8 !important; }

    /* 규격 고정 */
    :root {
        --side-margin: 60px;
        --grid-gap: 20px;
    }

    /* 상단 전체 고정 영역 배경 (블러) */
    .header-bg {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 220px; /* 필터 포함 높이 */
        background-color: rgba(242, 245, 248, 0.9);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        z-index: 999;
        padding: 30px var(--side-margin) 0 var(--side-margin);
    }

    .main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.2px; }
    .sub-title { color: #6A7683; margin: 5px 0 10px 0; font-weight: 500; font-size: 0.85rem; }

    /* 월 헤더 그리드 고정 */
    .month-container {
        position: fixed;
        top: 170px; /* 타이틀 + 필터 아래 위치 */
        left: var(--side-margin);
        right: var(--side-margin);
        z-index: 1001;
    }

    .roadmap-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: var(--grid-gap);
        width: 100%;
    }

    .month-label { 
        background-color: #FFFFFF; color: #1A1A1A; padding: 10px; border-radius: 12px; 
        font-weight: 800; font-size: 0.9rem; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    }

    /* 본문 카드 영역 (상단 높이만큼 밀착) */
    .main-content-area {
        margin-top: 235px; 
        padding: 0 var(--side-margin) 60px var(--side-margin);
    }

    /* 카드 디자인 */
    .project-card { 
        background-color: #FFFFFF !important; border-radius: 20px; 
        border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 8px; overflow: hidden; transition: transform 0.2s ease;
    }
    .project-card:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

    summary { list-style: none; padding: 14px 18px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
    summary::-webkit-details-marker { display: none; }
    .card-project-title { font-size: 1.05rem; font-weight: 800; color: #1A1A1A; }
    .card-content { padding: 0 18px 18px 18px; }
    .card-desc { font-size: 0.85rem; line-height: 1.5; margin: 6px 0; color: #333; font-weight: 500; }
    .card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.6; margin: 0; }

    .arrow-icon { width: 8px; height: 8px; border-top: 2px solid #BCB8AD; border-right: 2px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }

    .badge-wrapper { display: flex; gap: 4px; margin-top: 4px; }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; }

    /* 필터 위젯 강제 고정 스타일 */
    .filter-sticky {
        position: fixed;
        top: 105px;
        left: 60px;
        right: 60px;
        z-index: 1002;
    }
    /* 필터 내부 여백 제거 */
    div[data-testid="stFormSubmitButton"] { display: none; }
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

# 4. 상단 고정 요소 (HTML)
st.markdown("""
<div class="header-bg">
    <div class="main-title">한빛앤 프로덕트 로드맵</div>
    <div class="sub-title">2026 상반기 마일스톤 타임라인</div>
</div>
<div class="month-container">
    <div class="roadmap-grid">
        <div class="month-label">1월</div><div class="month-label">2월</div>
        <div class="month-label">3월</div><div class="month-label">4월</div>
        <div class="month-label">5월</div><div class="month-label">6월</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. 필터 위젯 (Streamlit 위젯을 특정 위치에 강제 고정)
st.markdown('<div class="filter-sticky">', unsafe_allow_html=True)
cat_list = list(COLOR_PALETTE.keys())
selected_cats = st.multiselect(
    "카테고리 필터", 
    options=cat_list, 
    default=cat_list, 
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# 6. 필터링 적용
filtered_df = df[df['Category'].isin(selected_cats)] if not df.empty else df

# 7. 본문 렌더링
if not filtered_df.empty:
    cards_html = '<div class="main-content-area"><div class="roadmap-grid">'
    for _, row in filtered_df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name = str(row['Category']).strip()
            status_text = str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
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
    st.markdown('<div class="main-content-area" style="text-align:center; padding-top:50px; color:#888;">표시할 프로젝트가 없습니다.</div>', unsafe_allow_html=True)
