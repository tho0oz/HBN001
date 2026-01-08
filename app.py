import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (Radius, Arrow, Hover 인터렉션)
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
.stApp { background-color: #F2F5F8; }
.main-title { font-size: 2.5rem; font-weight: 800; color: #1A1A1A; padding: 20px 0 5px 0; letter-spacing: -1.5px; }
.sub-title { color: #6A7683; margin-bottom: 40px; font-weight: 500; font-size: 0.9rem; }

/* 전체 그리드 컨테이너 */
.roadmap-container { 
    display: grid; 
    grid-template-columns: repeat(6, 1fr); 
    gap: 16px; 
    align-items: start; 
}

/* 월 헤더 스타일: 고정 */
.month-label { 
    background-color: #FFFFFF; 
    color: #1A1A1A; 
    padding: 12px; 
    border-radius: 16px; 
    font-weight: 800; 
    font-size: 1rem; 
    text-align: center; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    margin-bottom: 20px;
    position: sticky; 
    top: 10px;      
    z-index: 99;    
}

/* 프로젝트 카드 스타일 (Radius 22px 적용 및 Hover 효과) */
.project-card { 
    background-color: #FFFFFF !important; 
    border-radius: 22px; 
    border: 1px solid rgba(0,0,0,0.05); 
    box-shadow: 0 4px 12px rgba(0,0,0,0.02); 
    margin-bottom: 12px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Hover 시 효과: 살짝 떠오르고 그림자 깊어짐 */
.project-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.1);
}

/* 클릭 영역 (summary) */
summary {
    list-style: none; 
    padding: 24px;
    cursor: pointer;
    outline: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
summary::-webkit-details-marker { display: none; }

/* 화살표 아이콘 (CSS로 구현) */
.arrow-icon {
    width: 12px;
    height: 12px;
    border-top: 2.5px solid #BCB8AD;
    border-right: 2.5px solid #BCB8AD;
    transform: rotate(135deg); /* 아래 방향 화살표 */
    transition: transform 0.3s ease;
    margin-left: 10px;
}

/* 열렸을 때 화살표 회전 및 제목 굵기 강조 */
details[open] .arrow-icon {
    transform: rotate(-45deg); /* 위 방향 화살표 */
    border-color: #1A1A1A;
}
details[open] {
    background-color: #FFFFFF !important;
}

.card-project-title { font-size: 1.15rem; font-weight: 800; }

/* 본문 영역 */
.card-content { padding: 0 24px 24px 24px; animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

.card-desc { font-size: 0.95rem; line-height: 1.6; margin-top: 10px; margin-bottom: 20px; color: #1A1A1A; font-weight: 500; }
.card-manager { font-size: 0.8rem; font-weight: 400; color: #1A1A1A; opacity: 0.7; }

/* 뱃지 */
.badge-wrapper { display: flex; gap: 6px; margin-top: 10px; }
.badge { padding: 5px 14px; border-radius: 10px; font-size: 0.75rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드
COLOR_PALETTE = {
    "논의": {"main": "#495057"}, "기획": {"main": "#FF9500"}, "디자인": {"main": "#5E5CE6"},
    "개발": {"main": "#007AFF"}, "QA": {"main": "#34C759"}, "배포": {"main": "#FF2D55"},
    "Default": {"main": "#ADB5BD"}
}

@st.cache_data(ttl=5)
def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame()

df = load_data()

# 4. 화면 출력
st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 상반기 마일스톤 타임라인</div>', unsafe_allow_html=True)

if not df.empty:
    full_html = '<div class="roadmap-container">'
    for i in range(1, 7):
        full_html += f'<div class="month-label" style="grid-column: {i};">{i}월</div>'

    for _, row in df.iterrows():
        try:
            start, end = int(row['StartMonth']), int(row['EndMonth'])
            span = end - start + 1
            cat_name, status_text = str(row['Category']).strip(), str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            grid_pos = f"grid-column: {start} / span {span};"
            
            # 카드 HTML (Arrow icon 포함)
            card_html = (
                f'<details class="project-card" style="{grid_pos}">'
                f'<summary>'
                f'<div>'
                f'<div class="card-project-title" style="color: {theme["main"]};">{row["Project"]}</div>'
                f'<div class="badge-wrapper"><div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1.5px solid {theme["main"]}30;">{combined_label}</div></div>'
                f'</div>'
                f'<div class="arrow-icon"></div>'
                f'</summary>'
                f'<div class="card-content">'
                f'<div class="card-desc">{row["Description"]}</div>'
                f'<div class="card-manager">{row["Manager"]}</div>'
                f'</div>'
                f'</details>'
            )
            full_html += card_html
        except: continue

    full_html += '</div>'
    st.markdown(full_html, unsafe_allow_html=True)
