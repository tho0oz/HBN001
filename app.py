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

# 2. 디자인 CSS (카드 너비 고정 + 사이드바 고정 + 여백 리셋)
st.markdown("""<style>
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }

    /* [사용자 제공 패딩 로직 적용] */
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
    .static-header { width: 100%; padding: 20px 0 30px 0; }
    .main-title { font-size: 2rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.5px; }
    .sub-title { color: #6A7683; margin: 8px 0 0 0; font-weight: 500; font-size: 0.9rem; }

    /* [수정] 월 버튼 사이드바 고정 (Sticky) */
    .sticky-sidebar {
        position: -webkit-sticky;
        position: sticky;
        top: 30px; /* 스크롤 시 상단 여백 */
        display: flex;
        flex-direction: column;
        gap: 80px; /* 월 버튼 사이 간격 (수직 스패닝 높이와 맞춤) */
        padding-top: 10px;
        z-index: 99;
    }

    /* 월 버튼 디자인 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 14px !important;
        padding: 12px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        width: 80px !important; /* 월 버튼 너비 고정 */
        height: 60px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06) !important;
    }

    /* [수정] 카드 가로 너비 고정 및 그리드 배치 */
    .roadmap-content-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, 320px); /* 카드 너비를 320px로 고정 */
        grid-auto-rows: 140px; /* 수직 월 간격과 일치 */
        gap: 20px;
        align-items: start;
    }

    /* 고정형 프로젝트 카드 */
    .project-card { 
        width: 320px !important; /* 가로 너비 320px 고정 */
        background-color: #FFFFFF !important; 
        border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        padding: 24px;
        transition: all 0.2s ease;
        height: calc(100% - 10px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
    }
    .project-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }

    .card-project-title { font-size: 1.1rem; font-weight: 800; color: #1A1A1A; margin-bottom: 8px; line-height: 1.3; }
    .badge { padding: 4px 12px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; display: inline-block; }
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

# 4. 화면 출력 영역
if st.session_state.selected_month is None:
    st.markdown('<div class="static-header"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>', unsafe_allow_html=True)
else:
    if st.button("전체보기"):
        st.session_state.selected_month = None
        st.rerun()

# 5. 콘텐츠 렌더링
if not df.empty:
    if st.session_state.selected_month is None:
        # 레이아웃 분할 (사이드바 1 : 본문 10)
        col_side, col_main = st.columns([1, 10])
        
        with col_side:
            # 월 버튼 고정 컨테이너 시작
            st.write('<div class="sticky-sidebar">', unsafe_allow_html=True)
            for m in range(1, 7):
                if st.button(f"{m}월", key=f"btn_{m}"):
                    st.session_state.selected_month = m
                    st.rerun()
            st.write('</div>', unsafe_allow_html=True)
            
        with col_main:
            # 카드 너비가 고정된 그리드 시작
            card_grid_html = '<div class="roadmap-content-grid">'
            for _, row in df.iterrows():
                try:
                    start, end = int(row['StartMonth']), int(row['EndMonth'])
                    span = end - start + 1
                    cat = str(row['Category']).strip()
                    color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
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
        # 필터링 모드 (상하 정렬)
        m = st.session_state.selected_month
        st.markdown(f'<div style="font-size: 2rem; font-weight: 800; margin-bottom: 25px;">{m}월</div>', unsafe_allow_html=True)
        month_tasks = df[(df['StartMonth'] <= m) & (df['EndMonth'] >= m)]
        if not month_tasks.empty:
            for _, row in month_tasks.iterrows():
                cat = str(row['Category']).strip()
                color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                st.markdown(f'''
                <div class="project-card" style="height: auto; margin-bottom: 15px;">
                    <div class="card-project-title">{row['Project']}</div>
                    <div><div class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">{cat} {row['Status']}</div></div>
                </div>''', unsafe_allow_html=True)
        else:
            st.info("진행 중인 프로젝트가 없습니다.")
else:
    st.markdown('<div style="padding-top: 100px; text-align: center; color: #888;">데이터를 불러오는 중입니다...</div>', unsafe_allow_html=True)
