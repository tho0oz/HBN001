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

# 2. 디자인 CSS (사용자 제공 패딩 로직 + 수직 스패닝 그리드)
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
    .static-header { width: 100%; padding: 20px 0 30px 0; }
    .main-title { font-size: 2rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.5px; }
    .sub-title { color: #6A7683; margin: 8px 0 0 0; font-weight: 500; font-size: 0.9rem; }

    /* [수정] 월 버튼 디자인: 이전 카드 스타일로 회귀 & 호버 인터랙션 일치 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 14px !important;
        padding: 12px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
        height: 60px;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06) !important;
        border-color: rgba(0,0,0,0.1) !important;
    }

    /* [수정] 수직 타임라인 그리드 시스템 */
    .vertical-roadmap-grid {
        display: grid;
        grid-template-columns: 100px 1fr; /* 월 100px : 카드 1fr */
        grid-template-rows: repeat(6, minmax(120px, auto)); /* 각 월의 최소 높이 설정 */
        gap: 20px;
        align-items: start;
    }

    /* 프로젝트 카드: 수직으로 길어지는 기능 반영 */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        overflow: hidden; transition: all 0.2s ease;
        height: calc(100% - 10px); /* 그리드 칸에 꽉 차게 설정 */
        display: flex;
        flex-direction: column;
    }
    .project-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }

    summary { list-style: none; padding: 20px 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; outline: none; }
    .card-project-title { font-size: 1.15rem; font-weight: 800; color: #1A1A1A; margin: 0; }
    .card-content { padding: 0 24px 24px 24px; }
    .card-desc { font-size: 0.9rem; line-height: 1.6; color: #333; margin: 10px 0; font-weight: 500; }
    .card-manager { font-size: 0.8rem; color: #1A1A1A; opacity: 0.7; font-weight: 400; }
    .arrow-icon { width: 8px; height: 8px; border-top: 2.5px solid #BCB8AD; border-right: 2.5px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }
    .badge { padding: 4px 12px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; display: inline-block; margin-top: 8px; }

    /* 필터링 모드 전용 세로 리스트 */
    .filter-list { display: flex; flex-direction: column; gap: 16px; }
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

# 4. 화면 제어
if st.session_state.selected_month is None:
    st.markdown('<div class="static-header"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>', unsafe_allow_html=True)
else:
    if st.button("전체보기"):
        st.session_state.selected_month = None
        st.rerun()

# 5. 콘텐츠 렌더링
if not df.empty:
    # --- 전체 보기 모드 (수직 스패닝 그리드) ---
    if st.session_state.selected_month is None:
        # 하나의 큰 그리드 시작
        html_buffer = ['<div class="vertical-roadmap-grid">']
        
        # 월 버튼 배치 (1열)
        for m in range(1, 7):
            # Streamlit 버튼을 HTML 그리드와 연동하기 위해 컬럼 활용 (꼼수 방지)
            pass 

        # 스트림릿 내에서 HTML Grid와 Button을 혼용하기 위해 레이아웃을 다시 잡습니다.
        cols = st.columns([1, 10])
        
        with cols[0]:
            st.write('<div style="display: flex; flex-direction: column; gap: 80px; padding-top: 10px;">', unsafe_allow_html=True)
            for m in range(1, 7):
                if st.button(f"{m}월", key=f"btn_{m}"):
                    st.session_state.selected_month = m
                    st.rerun()
            st.write('</div>', unsafe_allow_html=True)
            
        with cols[1]:
            # 카드들을 렌더링 (이 카드들은 각자의 StartMonth와 EndMonth에 맞춰 높이가 결정됨)
            # 프로젝트들을 담을 컨테이너 (그리드)
            card_grid_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); grid-auto-rows: 140px; gap: 20px;">'
            
            for _, row in df.iterrows():
                try:
                    start = int(row['StartMonth'])
                    end = int(row['EndMonth'])
                    span = end - start + 1
                    cat = str(row['Category']).strip()
                    color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                    
                    # 수직 스패닝 계산 (CSS grid-row 사용)
                    # 140px는 월 버튼 간격과 맞춘 수치입니다.
                    grid_row_style = f"grid-row: {start} / span {span};"
                    
                    card_grid_html += f'''
                    <details class="project-card" style="{grid_row_style}">
                        <summary><div>
                            <div class="card-project-title">{row['Project']}</div>
                            <div class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">{cat} {row['Status']}</div>
                        </div><div class="arrow-icon"></div></summary>
                        <div class="card-content">
                            <div class="card-desc">{row['Description']}</div>
                            <div class="card-manager">{row['Manager']}</div>
                        </div>
                    </details>'''
                except: continue
            card_grid_html += '</div>'
            st.markdown(card_grid_html, unsafe_allow_html=True)

    # --- 특정 월 필터링 모드 (상하 정렬) ---
    else:
        m = st.session_state.selected_month
        st.markdown(f'<div style="font-size: 2rem; font-weight: 800; margin-bottom: 25px;">{m}월</div>', unsafe_allow_html=True)
        
        month_tasks = df[(df['StartMonth'] <= m) & (df['EndMonth'] >= m)]
        if not month_tasks.empty:
            html_str = '<div class="filter-list">'
            for _, row in month_tasks.iterrows():
                cat = str(row['Category']).strip()
                color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                html_str += f'''
                <details class="project-card"><summary><div>
                    <div class="card-project-title">{row['Project']}</div>
                    <div class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">{cat} {row['Status']}</div>
                </div><div class="arrow-icon"></div></summary>
                <div class="card-content"><div class="card-desc">{row['Description']}</div><div class="card-manager">{row['Manager']}</div></div>
                </details>'''
            html_str += '</div>'
            st.markdown(html_str, unsafe_allow_html=True)
        else:
            st.info("진행 중인 프로젝트가 없습니다.")
