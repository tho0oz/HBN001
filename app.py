import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# [상태 관리] 선택된 월 저장
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = None

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (고밀도 여백 + 수직 높이 동기화 + 상단 정렬)
st.markdown("""<style>
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }

    /* [사용자 제공 패딩 로직] */
    .st-emotion-cache-zy6yx3 {
        width: 100% !important;
        max-width: initial !important;
        min-width: auto !important;
        padding-top: 2rem !important;
    }
    @media (min-width: calc(736px + 8rem)) {
        .st-emotion-cache-zy6yx3 {
            padding-left: 3.2rem !important;
            padding-right: 3.2rem !important;
        }
    }

    .stApp { background-color: #F2F5F8 !important; }

    /* 헤더 스타일 */
    .static-header { width: 100%; padding: 20px 0 20px 0; }
    .main-title { font-size: 2rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.5px; }
    .sub-title { color: #6A7683; margin: 8px 0 0 0; font-weight: 500; font-size: 0.9rem; }

    /* [수정] 월 버튼 사이드바 고정 및 높이 동기화 */
    .sticky-sidebar {
        position: -webkit-sticky;
        position: sticky;
        top: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px; /* 카드 그리드 gap과 일치 */
        z-index: 99;
    }

    /* [수정] 월 버튼: 높이를 1개월 카드 높이(110px)와 동일하게 설정 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 14px !important;
        padding: 0 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        width: 80px !important;
        height: 110px !important; /* 1개월 카드 높이와 동일 */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06) !important;
    }

    /* [수정] 카드 그리드: 높이 규격화 (110px) */
    .roadmap-content-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, 320px);
        grid-auto-rows: 110px; /* 월 버튼 높이와 일치 */
        gap: 15px;
        align-items: start;
    }

    /* [수정] 프로젝트 카드: 내부 여백 최소화 및 상단 정렬 */
    .project-card { 
        width: 320px !important;
        background-color: #FFFFFF !important; 
        border-radius: 22px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        padding: 12px 16px !important; /* 여백 최소화 */
        transition: all 0.2s ease;
        height: calc(100% - 2px);
        display: flex;
        flex-direction: column;
        justify-content: flex-start !important; /* 상단 정렬 */
        box-sizing: border-box;
    }
    .project-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }

    .card-project-title { 
        font-size: 1rem; 
        font-weight: 800; 
        color: #1A1A1A; 
        margin-bottom: 6px; 
        line-height: 1.3;
        text-align: left;
    }
    .badge { padding: 3px 10px; border-radius: 7px; font-size: 0.65rem; font-weight: 700; display: inline-block; }
</style>""", unsafe_allow_html=True)

# 3. 데이터 로드
COLOR_PALETTE = {
    "논의": "#495057", "기획": "#FF9500", "디자인": "#5E5CE6",
    "개발": "#007AFF", "QA": "#34C759", "배포": "#FF2D55", "Default": "#ADB5BD"
}

@st.cache_data(ttl=5)
def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame()

df = load_data()

# 4. 화면 출력
if st.session_state.selected_month is None:
    st.markdown('<div class="static-header"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>', unsafe_allow_html=True)
else:
    if st.button("전체보기"):
        st.session_state.selected_month = None
        st.rerun()

# 5. 콘텐츠 렌더링
if not df.empty:
    if st.session_state.selected_month is None:
        col_side, col_main = st.columns([1, 12])
        
        with col_side:
            st.write('<div class="sticky-sidebar">', unsafe_allow_html=True)
            for m in range(1, 7):
                if st.button(f"{m}월", key=f"btn_{m}"):
                    st.session_state.selected_month = m
                    st.rerun()
            st.write('</div>', unsafe_allow_html=True)
            
        with col_main:
            card_grid_html = '<div class="roadmap-content-grid">'
            for _, row in df.iterrows():
                try:
                    start, end = int(row['StartMonth']), int(row['EndMonth'])
                    span = end - start + 1
                    cat = str(row['Category']).strip()
                    color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                    
                    # 수직 스패닝 (StartMonth 위치에서 Span만큼)
                    grid_row_style = f"grid-row: {start} / span {span};"
                    
                    card_grid_html += f'''
                    <div class="project-card" style="{grid_row_style}">
                        <div class="card-project-title">{row['Project']}</div>
                        <div><div class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">{cat} {row['Status']}</div></div>
                    </div>'''
                except: continue
            card_grid_html += '</div>'
            st.markdown(card_grid_html, unsafe_allow_html=True)

    else:
        m = st.session_state.selected_month
        st.markdown(f'<div style="font-size: 2rem; font-weight: 800; margin-bottom: 25px;">{m}월</div>', unsafe_allow_html=True)
        month_tasks = df[(df['StartMonth'] <= m) & (df['EndMonth'] >= m)]
        if not month_tasks.empty:
            for _, row in month_tasks.iterrows():
                cat = str(row['Category']).strip()
                color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                st.markdown(f'''
                <div class="project-card" style="height: auto; margin-bottom: 15px; width: 100% !important;">
                    <div class="card-project-title">{row['Project']}</div>
                    <div><div class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">{cat} {row['Status']}</div></div>
                </div>''', unsafe_allow_html=True)
else:
    st.info("데이터 로딩 중...")
