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

# 2. 디자인 CSS
st.markdown("""<style>
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }

    .st-emotion-cache-zy6yx3 {
        width: 100% !important;
        max-width: initial !important;
        padding-top: 2rem !important;
    }

    .stApp { background-color: #F2F5F8 !important; }

    /* 헤더 스타일 */
    .static-header { width: 100%; padding: 0 0 30px 0; }
    .main-title { font-size: 2rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.5px; }
    
    /* 월 버튼 영역 */
    .month-button-container {
        display: flex;
        flex-direction: column;
        gap: 15px; /* 그리드 gap과 일치 */
    }

    /* 버튼 스타일 수정: 높이를 카드와 맞춤 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 14px !important;
        padding: 0 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        height: 120px !important; /* 카드 기본 높이와 일치 */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        background-color: #f8f9fa !important;
    }

    /* 좌우 스크롤이 가능한 로드맵 컨테이너 */
    .roadmap-scroll-wrapper {
        overflow-x: auto;
        white-space: nowrap;
        padding-bottom: 20px;
        -webkit-overflow-scrolling: touch;
    }

    /* 수직 타임라인 그리드 시스템 */
    .vertical-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, 280px); /* 카드 너비 고정 */
        grid-template-rows: repeat(6, 120px); /* 1~6월 높이 고정 */
        grid-auto-flow: column; /* 카드가 쌓이지 않고 옆으로 나열되도록 설정 */
        gap: 15px;
        min-width: 100%;
    }

    /* 프로젝트 카드 스타일 (단순화) */
    .project-card-simple { 
        background-color: #FFFFFF !important; 
        border-radius: 18px; 
        border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        padding: 18px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.2s ease;
        overflow: hidden;
    }
    .project-card-simple:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }

    .card-project-title { 
        font-size: 1rem; 
        font-weight: 800; 
        color: #1A1A1A; 
        margin-bottom: 8px;
        white-space: normal;
        line-height: 1.3;
    }
    
    .badge { 
        padding: 4px 10px; 
        border-radius: 8px; 
        font-size: 0.7rem; 
        font-weight: 700; 
        display: inline-block;
    }

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
    st.markdown('<div class="static-header"><div class="main-title">한빛앤 프로덕트 로드맵</div></div>', unsafe_allow_html=True)
else:
    if st.button("← 전체보기"):
        st.session_state.selected_month = None
        st.rerun()

# 5. 콘텐츠 렌더링
if not df.empty:
    if st.session_state.selected_month is None:
        # 좌측 월 버튼 + 우측 로드맵 그리드
        cols = st.columns([0.8, 10])
        
        with cols[0]:
            st.write('<div class="month-button-container">', unsafe_allow_html=True)
            for m in range(1, 7):
                if st.button(f"{m}월", key=f"btn_{m}"):
                    st.session_state.selected_month = m
                    st.rerun()
            st.write('</div>', unsafe_allow_html=True)
            
        with cols[1]:
            # 좌우 스크롤 가능 영역 시작
            html_buffer = ['<div class="roadmap-scroll-wrapper"><div class="vertical-grid">']
            
            for _, row in df.iterrows():
                try:
                    start = int(row['StartMonth'])
                    end = int(row['EndMonth'])
                    span = end - start + 1
                    # 1~6월 범위를 벗어나는 데이터 방지
                    if start < 1 or start > 6: continue
                    
                    cat = str(row['Category']).strip()
                    color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                    
                    # grid-row: 시작줄 / span 칸수
                    grid_row_style = f"grid-row: {start} / span {span};"
                    
                    card_html = f'''
                    <div class="project-card-simple" style="{grid_row_style}">
                        <div class="card-project-title">{row['Project']}</div>
                        <div>
                            <span class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">
                                {cat} · {row['Status']}
                            </span>
                        </div>
                    </div>'''
                    html_buffer.append(card_html)
                except: continue
                
            html_buffer.append('</div></div>')
            st.markdown("".join(html_buffer), unsafe_allow_html=True)

    # --- 특정 월 필터링 모드 ---
    else:
        m = st.session_state.selected_month
        st.markdown(f'<div style="font-size: 2rem; font-weight: 800; margin-bottom: 25px;">{m}월 진행 프로젝트</div>', unsafe_allow_html=True)
        
        month_tasks = df[(df['StartMonth'] <= m) & (df['EndMonth'] >= m)]
        if not month_tasks.empty:
            html_str = '<div class="filter-list">'
            for _, row in month_tasks.iterrows():
                cat = str(row['Category']).strip()
                color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                html_str += f'''
                <div class="project-card-simple" style="min-height: 100px;">
                    <div class="card-project-title" style="font-size: 1.2rem;">{row['Project']}</div>
                    <div>
                        <span class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">
                            {cat} · {row['Status']}
                        </span>
                    </div>
                </div>'''
            html_str += '</div>'
            st.markdown(html_str, unsafe_allow_html=True)
        else:
            st.info("해당 월에 진행 중인 프로젝트가 없습니다.")
