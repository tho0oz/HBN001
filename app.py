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
[data-testid="stSidebar"] {display: none;}
.stApp { background-color: #F2F5F8; }
.main-title { font-size: 2.5rem; font-weight: 800; color: #1A1A1A; padding: 20px 0 5px 0; letter-spacing: -1.5px; }
.sub-title { color: #6A7683; margin-bottom: 40px; font-weight: 500; font-size: 0.9rem; }
.roadmap-container { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; align-items: start; }
.month-label { background-color: #FFFFFF; color: #1A1A1A; padding: 12px; border-radius: 12px; font-weight: 800; font-size: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 20px; }
.project-card { background-color: #FFFFFF !important; border-radius: 18px; padding: 22px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 4px 12px rgba(0,0,0,0.02); display: flex; flex-direction: column; margin-bottom: 12px; }
.card-project-title { font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; }
.card-desc { font-size: 0.9rem; line-height: 1.5; margin-bottom: 18px; color: #1A1A1A; font-weight: 500; }
.card-manager { font-size: 0.75rem; font-weight: 400; color: #1A1A1A; opacity: 0.7; margin-bottom: 18px; }
.badge-wrapper { display: flex; gap: 6px; }
.badge { padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 및 컬러 설정
COLOR_PALETTE = {
    "논의": {"main": "#495057"}, "기획": {"main": "#FF9500"}, "디자인": {"main": "#5E5CE6"},
    "개발": {"main": "#007AFF"}, "QA": {"main": "#34C759"}, "배포": {"main": "#FF2D55"},
    "Default": {"main": "#ADB5BD"}
}

@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame()

df = load_data()

# 4. 화면 출력
st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 상반기 마일스톤 타임라인</div>', unsafe_allow_html=True)

if not df.empty:
    full_html = '<div class="roadmap-container">'
    
    # 월 헤더 추가
    for i in range(1, 7):
        full_html += f'<div class="month-label" style="grid-column: {i};">{i}월</div>'

    # 프로젝트 카드 추가
    for _, row in df.iterrows():
        try:
            start = int(row['StartMonth'])
            end = int(row['EndMonth'])
            span = end - start + 1
            cat_name = str(row['Category']).strip()
            status_text = str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            
            # 통합 뱃지 텍스트 생성 (예: 개발 진행중)
            combined_status = f"{cat_name} {status_text}"
            
            grid_pos = f"grid-column: {start} / span {span};"
            
            # 카드 HTML 생성 (기간 텍스트 제거 및 뱃지 통합)
            card_html = (
                f'<div class="project-card" style="{grid_pos}">'
                f'<div class="card-project-title" style="color: {theme["main"]};">{row["Project"]}</div>'
                f'<div class="card-desc">{row["Description"]}</div>'
                f'<div class="card-manager">{row["Manager"]}</div>'
                f'<div class="badge-wrapper">'
                f'<div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1.5px solid {theme["main"]}30;">{combined_status}</div>'
                f'</div></div>'
            )
            full_html += card_html
        except:
            continue

    full_html += '</div>'
    st.markdown(full_html, unsafe_allow_html=True)
else:
    st.info("데이터를 불러오는 중이거나 시트가 비어있습니다.")
