import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# [상태 관리] 선택된 월 저장 (기본값: None - 전체 보기)
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = None

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (사용자 제공 패딩 및 가로 정렬 스타일)
st.markdown("""<style>
    header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }

    /* 사용자 제공 패딩 로직 */
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

    /* 월 버튼 스타일 (필터) */
    .stButton > button {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 14px !important;
        padding: 12px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { transform: translateY(-2px); border-color: #1A1A1A !important; }

    /* 가로 정렬 컨테이너 (한 줄 정렬용) */
    .horizontal-scroll-wrapper {
        display: flex;
        flex-direction: row;
        overflow-x: auto;
        gap: 20px;
        padding: 10px 5px 30px 5px;
        width: 100%;
    }
    .horizontal-scroll-wrapper .project-card {
        min-width: 350px; /* 가로 모드일 때 카드 최소 너비 */
        flex: 0 0 auto;
    }

    /* 세로 리스트 정렬 (전체 보기용) */
    .vertical-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; align-items: start; }

    /* 카드 디자인 */
    .project-card { 
        background-color: #FFFFFF !important; 
        border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        overflow: hidden; margin-bottom: 12px;
    }
    summary { list-style: none; padding: 20px 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; outline: none; }
    .card-project-title { font-size: 1.15rem; font-weight: 800; color: #1A1A1A; margin: 0; }
    .card-content { padding: 0 24px 24px 24px; }
    .card-desc { font-size: 0.9rem; line-height: 1.6; color: #333; margin: 10px 0; font-weight: 500; }
    .card-manager { font-size: 0.8rem; color: #1A1A1A; opacity: 0.7; font-weight: 400; }
    .arrow-icon { width: 8px; height: 8px; border-top: 2.5px solid #BCB8AD; border-right: 2.5px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }
    .badge { padding: 4px 12px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; display: inline-block; margin-top: 8px; }
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

# 4. 상단 헤더
st.markdown('<div class="static-header"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>', unsafe_allow_html=True)

# [상단 내비게이션] 전체 보기 버튼
if st.session_state.selected_month is not None:
    if st.button("← 전체 보기로 돌아가기"):
        st.session_state.selected_month = None
        st.rerun()

# 5. 메인 콘텐츠 렌더링
if not df.empty:
    # --- 전체 보기 모드 ---
    if st.session_state.selected_month is None:
        for m in range(1, 7):
            col_left, col_right = st.columns([1, 10])
            with col_left:
                if st.button(f"{m}월", key=f"btn_{m}"):
                    st.session_state.selected_month = m
                    st.rerun()
            
            with col_right:
                month_tasks = df[df['StartMonth'] == m]
                if not month_tasks.empty:
                    html_str = '<div class="vertical-list">'
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
                    st.markdown('<p style="color:#BCB8AD; font-size:0.85rem; padding-top:15px;">예정된 프로젝트 없음</p>', unsafe_allow_html=True)
            st.write("") # 간격

    # --- 특정 월 필터링 모드 (한 줄 정렬) ---
    else:
        m = st.session_state.selected_month
        st.markdown(f"### 📅 {m}월 마일스톤 상세")
        
        month_tasks = df[df['StartMonth'] == m]
        if not month_tasks.empty:
            html_str = '<div class="horizontal-scroll-wrapper">'
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
            st.info("해당 월에 데이터가 없습니다.")

else:
    st.markdown('<div class="main-content">데이터 로딩 중...</div>', unsafe_allow_html=True)
