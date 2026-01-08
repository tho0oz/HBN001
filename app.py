import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (줄바꿈/들여쓰기 제거)
st.markdown("""<style>
header, [data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
.stApp { background-color: #F2F5F8 !important; }
.roadmap-outer-wrapper { min-width: 1500px; padding: 40px 60px; box-sizing: border-box; }
.header-area { margin-bottom: 30px; }
.main-title { font-size: 2.2rem; font-weight: 800; color: #1A1A1A; letter-spacing: -1.5px; margin: 0; }
.sub-title { color: #6A7683; font-size: 0.9rem; margin-top: 8px; font-weight: 500; }
.roadmap-main-grid { display: grid; grid-template-columns: 100px repeat(3, 1fr); grid-template-rows: repeat(6, 180px); gap: 20px; width: 100%; position: relative; }
.month-btn { background-color: #FFFFFF; color: #1A1A1A; border-radius: 16px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.03); grid-column: 1; z-index: 5; }
.project-card { background-color: #FFFFFF !important; border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 4px 12px rgba(0,0,0,0.02); transition: all 0.3s ease; overflow: hidden; display: flex; flex-direction: column; z-index: 10; }
.project-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); z-index: 20; }
summary { list-style: none; padding: 22px; cursor: pointer; display: flex; justify-content: space-between; align-items: flex-start; outline: none; }
summary::-webkit-details-marker { display: none; }
.card-project-title { font-size: 1.15rem; font-weight: 800; color: #1A1A1A; line-height: 1.3; }
.card-content { padding: 0 22px 22px 22px; }
.card-desc { font-size: 0.9rem; line-height: 1.5; color: #333; margin: 8px 0; font-weight: 500; }
.card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.6; margin-top: 10px; font-weight: 400; }
.arrow-icon { width: 9px; height: 9px; border-top: 2.5px solid #BCB8AD; border-right: 2.5px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; margin-top: 6px; }
details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }
.badge { padding: 4px 12px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; display: inline-block; margin-top: 8px; }
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
    try:
        df = pd.read_csv(SHEET_URL)
        return df.dropna(subset=['StartMonth', 'EndMonth'])
    except:
        return pd.DataFrame()

df = load_data()

# 4. 콘텐츠 빌드
if not df.empty:
    header_html = '<div class="roadmap-outer-wrapper"><div class="header-area"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>'
    grid_html = '<div class="roadmap-main-grid">'
    
    # (1) 월 레이블 배치
    for m in range(1, 7):
        grid_html += f'<div class="month-btn" style="grid-row:{m};">{m}월</div>'
    
    # (2) 겹침 방지 배치 알고리즘
    # 3개의 데이터 열(column 2, 3, 4)이 각 월(1~6)에 비어있는지 체크하는 표
    slots = {2: [False]*7, 3: [False]*7, 4: [False]*7}
    
    for _, row in df.iterrows():
        try:
            start = int(row['StartMonth'])
            end = int(row['EndMonth'])
            span = end - start + 1
            cat = str(row['Category']).strip()
            color = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
            
            # 들어갈 수 있는 가장 왼쪽 열 찾기
            target_col = 2
            for col in [2, 3, 4]:
                # 시작월부터 종료월까지 해당 열이 비어있는지 확인
                if not any(slots[col][m] for m in range(start, end + 1)):
                    target_col = col
                    # 찾은 빈자리에 프로젝트 점유 표시
                    for m in range(start, end + 1):
                        slots[col][m] = True
                    break
            
            card = f'<details class="project-card" style="grid-row:{start}/span {span};grid-column:{target_col};">'
            card += f'<summary><div><div class="card-project-title">{row["Project"]}</div>'
            card += f'<div class="badge" style="background-color:{color}15;color:{color};border:1.5px solid {color}30;">{cat} {row["Status"]}</div>'
            card += f'</div><div class="arrow-icon"></div></summary>'
            card += f'<div class="card-content"><div class="card-desc">{row["Description"]}</div>'
            card += f'<div class="card-manager">{row["Manager"]}</div></div></details>'
            grid_html += card
        except: continue

    grid_html += '</div></div>'
    st.markdown((header_html + grid_html).replace("\n", ""), unsafe_allow_html=True)
else:
    st.info("데이터를 불러올 수 없습니다. 구글 시트의 날짜 형식을 확인해주세요.")
