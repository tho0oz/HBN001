import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (들여쓰기/줄바꿈 없이 압축형태로 작성)
st.markdown("""<style>
header, [data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
[class*="st-emotion-cache"] { padding: 0 !important; max-width: 100% !important; }
.stApp { background-color: #F2F5F8 !important; }
.roadmap-outer-wrapper { min-width: 1400px; padding: 40px 60px; box-sizing: border-box; overflow-x: auto; }
.header-area { margin-bottom: 40px; }
.main-title { font-size: 2.2rem; font-weight: 800; color: #1A1A1A; letter-spacing: -1.5px; margin: 0; }
.sub-title { color: #6A7683; font-size: 0.9rem; margin-top: 8px; font-weight: 500; }
.roadmap-main-grid { display: grid; grid-template-columns: 100px 1fr 1fr 1fr; grid-template-rows: repeat(6, 180px); gap: 20px; width: 100%; position: relative; }
.month-btn { background-color: #FFFFFF; color: #1A1A1A; border-radius: 16px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.03); grid-column: 1; }
.project-card { background-color: #FFFFFF !important; border-radius: 24px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 4px 12px rgba(0,0,0,0.02); transition: all 0.3s ease; overflow: hidden; display: flex; flex-direction: column; }
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
::-webkit-scrollbar { height: 10px; }
::-webkit-scrollbar-track { background: #F2F5F8; }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 10px; }
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

# 4. 콘텐츠 빌드 (코드 노출 방지를 위해 줄바꿈/공백 제거)
if not df.empty:
    # 제목 영역
    header_html = '<div class="roadmap-outer-wrapper"><div class="header-area"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>'
    
    # 그리드 시작
    grid_html = '<div class="roadmap-main-grid">'
    
    # (1) 월 레이블
    for m in range(1, 7):
        grid_html += f'<div class="month-btn" style="grid-row:{m};">{m}월</div>'
    
    # (2) 프로젝트 카드
    task_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    cols = [2, 3, 4] # 카드 배치용 열

    for _, row in df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat = str(row['Category']).strip()
            color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
            
            # 수직 스패닝 및 가로 열 결정
            c_idx = task_counts[start] % 3
            col_pos = cols[c_idx]
            task_counts[start] += 1
            
            # 카드 HTML 조립 (들여쓰기 절대 금지)
            card = f'<details class="project-card" style="grid-row:{start}/span {span};grid-column:{col_pos};">'
            card += f'<summary><div><div class="card-project-title">{row["Project"]}</div>'
            card += f'<div class="badge" style="background-color:{color}15;color:{color};border:1.5px solid {color}30;">{cat} {row["Status"]}</div>'
            card += f'</div><div class="arrow-icon"></div></summary>'
            card += f'<div class="card-content"><div class="card-desc">{row["Description"]}</div>'
            card += f'<div class="card-manager">👤 {row["Manager"]}</div></div></details>'
            grid_html += card
        except: continue

    grid_html += '</div></div>'
    
    # 최종 결과물에서 혹시 모를 줄바꿈까지 한 번 더 제거하여 출력
    st.markdown((header_html + grid_html).replace("\n", ""), unsafe_allow_html=True)
else:
    st.info("데이터를 불러올 수 없습니다.")
