import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 강력한 레이아웃 초기화 및 타임라인 CSS
st.markdown("""
<style>
    /* [1] 스트림릿 모든 기본 여백 및 가로 제한 해제 */
    header, [data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
    [data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: visible !important; }
    [class*="st-emotion-cache"] { padding: 0 !important; max-width: 100% !important; overflow: visible !important; }
    .stApp { background-color: #F2F5F8 !important; overflow-x: auto !important; }

    /* [2] 가로 스크롤을 위한 전체 컨테이너 */
    .roadmap-outer-wrapper {
        min-width: 1400px; /* 노트북에서도 깨지지 않는 최소 가로 폭 */
        padding: 40px 60px;
        box-sizing: border-box;
    }

    /* 제목 영역 스타일 */
    .header-area { margin-bottom: 40px; }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1A1A1A; letter-spacing: -1.5px; margin: 0; }
    .sub-title { color: #6A7683; font-size: 0.9rem; margin-top: 8px; font-weight: 500; }

    /* [3] 수직 타임라인 그리드 (월 버튼 1열 + 프로젝트 3열) */
    .roadmap-main-grid {
        display: grid;
        grid-template-columns: 100px 1fr 1fr 1fr; /* 월 레이블(100px) + 프로젝트 카드 3열 */
        grid-template-rows: repeat(6, 180px); /* 1달당 높이 180px 고정 */
        gap: 20px;
        width: 100%;
    }

    /* 월 레이블 버튼 스타일 */
    .month-btn {
        background-color: #FFFFFF;
        color: #1A1A1A;
        border-radius: 16px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.03);
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        grid-column: 1; /* 무조건 첫 번째 열 */
    }
    .month-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }

    /* [4] 프로젝트 카드 디자인 및 수직 스패닝 */
    .project-card {
        background-color: #FFFFFF !important;
        border-radius: 24px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        z-index: 10;
    }
    .project-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); }

    summary { list-style: none; padding: 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: flex-start; outline: none; }
    summary::-webkit-details-marker { display: none; }
    .card-project-title { font-size: 1.2rem; font-weight: 800; color: #1A1A1A; line-height: 1.3; }
    
    .card-content { padding: 0 24px 24px 24px; }
    .card-desc { font-size: 0.95rem; line-height: 1.6; color: #333; margin: 10px 0; font-weight: 500; }
    .card-manager { font-size: 0.8rem; color: #1A1A1A; opacity: 0.6; margin-top: 15px; }

    .arrow-icon { width: 10px; height: 10px; border-top: 2.5px solid #BCB8AD; border-right: 2.5px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; margin-top: 8px; }
    details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }
    
    .badge { padding: 5px 14px; border-radius: 10px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-top: 10px; }

    /* 가로 스크롤바 디자인 */
    ::-webkit-scrollbar { height: 10px; }
    ::-webkit-scrollbar-track { background: #F2F5F8; }
    ::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 및 컬러 매핑
COLOR_PALETTE = {
    "논의": "#495057", "기획": "#FF9500", "디자인": "#5E5CE6",
    "개발": "#007AFF", "QA": "#34C759", "배포": "#FF2D55", "Default": "#ADB5BD"
}

@st.cache_data(ttl=5)
def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame()

df = load_data()

# 4. 전체 로드맵 렌더링
if not df.empty:
    # 전체를 감싸는 스크롤 wrapper
    html = '<div class="roadmap-outer-wrapper">'
    
    # 제목 영역
    html += '<div class="header-area"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>'
    
    # 그리드 시작
    html += '<div class="roadmap-main-grid">'
    
    # (1) 왼쪽 월 버튼 배치 (1행~6행)
    for m in range(1, 7):
        # 월 버튼은 각 행의 첫 번째 열에 고정
        html += f'<div class="month-btn" style="grid-row: {m};">{m}월</div>'
    
    # (2) 프로젝트 카드 배치 (수직 스패닝 반영)
    # 카드들이 겹치지 않게 하기 위해 열 번호를 관리합니다. (2, 3, 4열 중 하나 선택)
    column_tracker = [2, 3, 4] 
    task_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0} # 월별 카드 누적 확인용

    for idx, row in df.iterrows():
        try:
            start = int(row['StartMonth'])
            end = int(row['EndMonth'])
            span = end - start + 1
            cat = str(row['Category']).strip()
            color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
            
            # 카드가 위치할 열 결정 (월별로 3개씩 배치)
            col_pos = column_tracker[task_counts[start] % 3]
            task_counts[start] += 1
            
            # 스타일 설정 (grid-row: 시작 / span 기간, grid-column: 결정된 열)
            grid_style = f"grid-row: {start} / span {span}; grid-column: {col_pos};"
            
            html += f'''
            <details class="project-card" style="{grid_style}">
                <summary>
                    <div>
                        <div class="card-project-title">{row['Project']}</div>
                        <div class="badge" style="background-color: {color}15; color: {color}; border: 1.5px solid {color}30;">{cat} {row['Status']}</div>
                    </div>
                    <div class="arrow-icon"></div>
                </summary>
                <div class="card-content">
                    <div class="card-desc">{row['Description']}</div>
                    <div class="card-manager">👤 {row['Manager']}</div>
                </div>
            </details>
            '''
        except: continue

    html += '</div></div>' # grid, wrapper 종료
    st.markdown(html, unsafe_allow_html=True)
else:
    st.info("데이터를 불러오는 중입니다. 구글 시트를 확인해 주세요.")
