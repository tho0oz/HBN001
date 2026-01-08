import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (접이식 애니메이션 및 스타일 추가)
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

/* 월 헤더 스타일: 스크롤 시 상단 고정 */
.month-label { 
    background-color: #FFFFFF; 
    color: #1A1A1A; 
    padding: 12px; 
    border-radius: 12px; 
    font-weight: 800; 
    font-size: 1rem; 
    text-align: center; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    margin-bottom: 20px;
    position: sticky; 
    top: 10px;      
    z-index: 99;    
}

/* 접이식 프로젝트 카드 (details 태그) */
.project-card { 
    background-color: #FFFFFF !important; 
    border-radius: 18_px; 
    border: 1px solid rgba(0,0,0,0.05); 
    box-shadow: 0 4px 12px rgba(0,0,0,0.02); 
    margin-bottom: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
}

/* 클릭하는 영역 (summary 태그) */
summary {
    list-style: none; /* 기본 화살표 숨기기 */
    padding: 22px;
    cursor: pointer;
    outline: none;
}
summary::-webkit-details-marker { display: none; }

/* 접혔을 때 보이는 프로젝트 제목 */
.card-project-title { font-size: 1.15rem; font-weight: 800; margin-bottom: 0px; display: inline-block; }

/* 펼쳤을 때 나타나는 본문 영역 */
.card-content {
    padding: 0 22px 22px 22px;
}
.card-desc { font-size: 0.9rem; line-height: 1.5; margin-top: 10px; margin-bottom: 18px; color: #1A1A1A; font-weight: 500; }
.card-manager { font-size: 0.75rem; font-weight: 400; color: #1A1A1A; opacity: 0.7; margin-bottom: 18px; }

/* 뱃지 */
.badge-wrapper { display: flex; gap: 6px; margin-top: 10px; }
.badge { padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; display: inline-block; }

/* 펼쳐졌을 때의 스타일 변화 */
details[open] {
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}
details[open] .card-project-title {
    margin-bottom: 10px;
}
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
st.markdown('<div class="sub-title">2026 상반기 마일스톤 타임라인 (클릭 시 상세 보기)</div>', unsafe_allow_html=True)

if not df.empty:
    full_html = '<div class="roadmap-container">'
    
    # 1월부터 6월까지 헤더
    for i in range(1, 7):
        full_html += f'<div class="month-label" style="grid-column: {i};">{i}월</div>'

    # 프로젝트 카드 리스트 (접이식 구조)
    for _, row in df.iterrows():
        try:
            start = int(row['StartMonth'])
            end = int(row['EndMonth'])
            span = end - start + 1
            cat_name = str(row['Category']).strip()
            status_text = str(row['Status']).strip()
            theme = COLOR_PALETTE.get(cat_name, COLOR_PALETTE["Default"])
            combined_label = f"{cat_name} {status_text}"
            grid_pos = f"grid-column: {start} / span {span};"
            
            # HTML 구성 (details/summary 태그 사용)
            # summary 안에는 접혔을 때 보일 제목과 뱃지 배치
            # card-content 안에는 펼쳤을 때 보일 설명과 담당자 배치
            card_html = (
                f'<details class="project-card" style="{grid_pos}">'
                f'<summary>'
                f'<div class="card-project-title" style="color: {theme["main"]};">{row["Project"]}</div>'
                f'<div class="badge-wrapper"><div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1.5px solid {theme["main"]}30;">{combined_label}</div></div>'
                f'</summary>'
                f'<div class="card-content">'
                f'<div class="card-desc">{row["Description"]}</div>'
                f'<div class="card-manager">{row["Manager"]}</div>'
                f'</div>'
                f'</details>'
            )
            full_html += card_html
        except:
            continue

    full_html += '</div>'
    st.markdown(full_html, unsafe_allow_html=True)
else:
    st.info("데이터를 불러오는 중이거나 시트가 비어있습니다.")
