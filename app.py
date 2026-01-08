import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 타임라인 그리드 디자인 CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #F2F5F8; }
    
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1A1A1A; padding: 20px 0 5px 0; letter-spacing: -1.5px; }
    .sub-title { color: #6A7683; margin-bottom: 40px; font-weight: 500; }

    /* 타임라인 컨테이너 */
    .timeline-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr); /* 6개월 등분 */
        gap: 20px;
        position: relative;
        padding-top: 60px;
    }

    /* 월 헤더 레이어 */
    .month-header-row {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 20px;
        position: absolute;
        top: 0;
        width: 100%;
    }

    .month-header {
        background-color: #FFFFFF;
        color: #1A1A1A;
        padding: 12px;
        border-radius: 15px;
        font-weight: 800;
        font-size: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }

    /* 프로젝트 카드 박스 (가로로 길게 이어짐) */
    .project-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 10px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        z-index: 1;
        display: flex;
        flex-direction: column;
    }

    .card-project-title { font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; }
    .card-desc { font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; color: #1A1A1A; font-weight: 500; }
    
    /* 담당자 및 기간 텍스트 */
    .card-info-row { font-size: 0.75rem; font-weight: 400; color: #1A1A1A; opacity: 0.7; margin-bottom: 15px; display: flex; justify-content: space-between; }
    
    .badge-wrapper { display: flex; gap: 6px; }
    .badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=30)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        return pd.DataFrame()

# 카테고리 컬러
COLOR_PALETTE = {
    "논의": {"main": "#495057"}, "기획": {"main": "#FF9500"}, "디자인": {"main": "#5E5CE6"},
    "개발": {"main": "#007AFF"}, "QA": {"main": "#34C759"}, "배포": {"main": "#FF2D55"},
    "Default": {"main": "#ADB5BD"}
}

df = load_data()

if not df.empty:
    st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">2026 상반기 마일스톤 타임라인</div>', unsafe_allow_html=True)

    # 타임라인 그리드 시작
    html_content = '<div class="timeline-grid">'
    
    # 월 헤더 추가
    html_content += '<div class="month-header-row">'
    for m in range(1, 7):
        html_content += f'<div class="month-header">{m}월</div>'
    html_content += '</div>'

    # 프로젝트 카드 추가
    # 각 프로젝트를 순회하며 적절한 위치에 배치
    for index, row in df.iterrows():
        start = int(row['StartMonth'])
        end = int(row['EndMonth'])
        cat_name = str(row['Category']).strip()
        theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
        duration = f"{start}월 - {end}월"
        
        # 그리드 위치 계산 (column-start / column-end)
        # CSS Grid에서 end는 exclusive이므로 +1 해줍니다.
        grid_col_style = f"grid-column: {start} / {end + 1};"
        
        html_content += f"""
        <div class="project-card" style="{grid_col_style}">
            <div class="card-project-title" style="color: {theme['main']};">{row['Project']}</div>
            <div class="card-desc">{row['Description']}</div>
            <div class="card-info-row">
                <span>{row['Manager']}</span>
                <span>{duration}</span>
            </div>
            <div class="badge-wrapper">
                <div class="badge" style="background-color: {theme['main']}15; color: {theme['main']}; border: 1.5px solid {theme['main']}20;">{cat_name}</div>
                <div class="badge" style="background-color: {theme['main']}; color: white;">{row['Status']}</div>
            </div>
        </div>
        """
    
    html_content += '</div>'
    st.markdown(html_content, unsafe_allow_html=True)
else:
    st.warning("데이터를 불러올 수 없습니다. 구글 시트 주소와 공유 설정을 확인해 주세요.")
