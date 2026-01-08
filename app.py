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
    /* [1] 스트림릿 내부 반응형 패딩 및 마진 완전 박멸 */
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
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
        --grid-column-gap: 20px;
        --grid-row-gap: 8px;
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

    /* 그리드 레이아웃 */
    .roadmap-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        column-gap: var(--grid-column-gap);
        row-gap: var(--grid-row-gap);
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
        margin-top: 155px; /* 헤더 높이만큼 띄움 */
        padding: 0 var(--side-margin) 60px var(--side-margin);
        width: 100%;
        box-sizing: border-box;
    }

    /* 필터 영역 스타일 */
    .filter-section {
        margin-bottom: 20px;
        padding: 10px 0;
    }

    /* 카드 디자인 */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 20px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 0 !important;
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
    
    /* 필터 멀티셀렉트 커스텀 */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
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

# 4. 상단 고정 영역
st.markdown(f"""
<div class="sticky-top-area">
    <div class="main-title">한빛앤 프로덕트 로드맵</div>
    <div class="sub-title">2026 상반기 마일스톤 타임라인</div>
    <div class="roadmap-grid">
        <div class="month-label">1월</div><div class="month-label">2월</div>
        <div class="month-label">3월</div><div class="month-label">4월</div>
        <div class="month-label">5월</div><div class="month-label">6월</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. 메인 본문 영역 시작
if not df.empty:
    # 필터 및 카드를 감싸는 컨테이너 시작
    st.markdown('<div class="main-content-area">', unsafe_allow_html=True)
    
    # --- 필터 섹션 ---
    # 실제 데이터에서 카테고리 추출
    available_categories = sorted(df['Category'].unique().tolist())
    
    # 필터 위젯 배치 (Streamlit 기본 위젯 사용)
    selected_categories = st.multiselect(
        "카테고리 필터",
        options=available_categories,
        default=available_categories,
        placeholder="카테고리를 선택하세요",
        label_visibility="collapsed" # 레이블 숨김
    )
    
    # 데이터 필터링
    filtered_df = df[df['Category'].isin(selected_categories)]
    
    st.markdown('<div class="filter-section"></div>', unsafe_allow_html=True)
    
    # --- 로드맵 카드 그리드 ---
    st.markdown('<div class="roadmap-grid">', unsafe_allow_html=True)
    
    for _, row in filtered_df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            grid_pos = f"grid-column: {start} / span {span};"
            
            cards_html = (
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
            st.markdown(cards_html, unsafe_allow_html=True)
        except: continue
        
    st.markdown('</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-content-area"><p>데이터를 불러올 수 없습니다.</p></div>', unsafe_allow_html=True)
