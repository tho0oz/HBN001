import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (필터 위젯 스타일 및 고정 영역 최적화)
st.markdown("""
<style>
    /* 스트림릿 기본 UI 초기화 */
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stAppViewBlockContainer"], [data-testid="stVerticalBlock"], [class*="st-emotion-cache"] {
        padding: 0 !important; margin: 0 !important; max-width: 100% !important;
    }
    .stApp { background-color: #F2F5F8 !important; }

    /* 규격 설정 */
    :root {
        --side-margin: 60px;
        --grid-column-gap: 20px;
        --grid-row-gap: 8px;
    }

    /* 상단 고정 영역 (높이 조정) */
    .sticky-top-area {
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 1000;
        background-color: rgba(242, 245, 248, 0.9);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 25px var(--side-margin) 15px var(--side-margin);
        box-sizing: border-box;
    }

    .main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.2px; }
    .sub-title { color: #6A7683; margin: 5px 0 15px 0; font-weight: 500; font-size: 0.85rem; }

    /* 필터 위젯 위치 조정을 위한 컨테이너 */
    .filter-container { margin-bottom: 20px; }

    /* 월 헤더 그리드 */
    .roadmap-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        column-gap: var(--grid-column-gap);
        row-gap: var(--grid-row-gap);
        width: 100%;
        box-sizing: border-box;
    }

    .month-label { 
        background-color: #FFFFFF; color: #1A1A1A; padding: 10px; border-radius: 12px; 
        font-weight: 800; font-size: 0.9rem; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    }

    /* 본문 영역 (필터 추가로 높이 증가 대응) */
    .main-content-area {
        margin-top: 230px; /* 필터 위젯 공간 확보를 위해 증가 */
        padding: 0 var(--side-margin) 60px var(--side-margin);
        width: 100%;
        box-sizing: border-box;
    }

    /* 카드 디자인 */
    .project-card { 
        background-color: #FFFFFF !important; border-radius: 20px; 
        border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 0 !important; overflow: hidden;
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
    
    /* 필터(Multiselect) 커스텀 스타일 */
    .stMultiSelect div[data-baseweb="select"] {
        border-radius: 10px;
        background-color: white;
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

# 4. 상단 고정 영역 및 필터 위젯
# HTML로 배경을 먼저 깔아주고 그 위에 Streamlit 위젯을 올립니다.
st.markdown(f"""
<div class="sticky-top-area">
    <div class="main-title">한빛앤 프로덕트 로드맵</div>
    <div class="sub-title">2026 상반기 마일스톤 타임라인</div>
    <div id="filter-anchor"></div>
</div>
""", unsafe_allow_html=True)

# 고정 영역 내부에 필터를 배치하기 위해 빈 컨테이너와 컬럼 활용
with st.container():
    # 고정 영역의 좌우 여백과 맞추기 위해 columns 사용
    _, col, _ = st.columns([0.05, 0.9, 0.05]) 
    with col:
        # 필터 위젯 (상단 고정 영역 위에 떠 있도록 처리)
        st.markdown('<div style="position:fixed; top:95px; left:60px; right:60px; z-index:1001;">', unsafe_allow_html=True)
        categories = ["전체"] + list(COLOR_PALETTE.keys())
        selected_cats = st.multiselect("", options=categories, default=["전체"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

# 월 헤더 (필터 아래에 배치)
st.markdown(f"""
<div style="position:fixed; top:165px; left:60px; right:60px; z-index:1000; width:calc(100% - 120px);">
    <div class="roadmap-grid">
        <div class="month-label">1월</div><div class="month-label">2월</div>
        <div class="month-label">3월</div><div class="month-label">4월</div>
        <div class="month-label">5월</div><div class="month-label">6월</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. 데이터 필터링 로직
if "전체" not in selected_cats:
    filtered_df = df[df['Category'].isin(selected_cats)]
else:
    filtered_df = df

# 6. 메인 본문 영역
if not filtered_df.empty:
    cards_html = '<div class="main-content-area"><div class="roadmap-grid">'
    for _, row in filtered_df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
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
    st.markdown('<div class="main-content-area" style="text-align:center; color:#888;">해당 카테고리에 프로젝트가 없습니다.</div>', unsafe_allow_html=True)
