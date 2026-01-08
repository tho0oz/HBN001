import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (사용자 제공 패딩 값 및 헤더 고정 해제 반영)
st.markdown("""<style>
/* 스트림릿 기본 UI 숨기기 */
header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }

/* [사용자 제안] 스트림릿 내부 컨테이너 여백 및 너비 강제 조정 */
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

/* [수정] 상단 헤더: 포지션 고정 제거 */
.static-header { 
    width: 100%;
    padding: 20px 0 30px 0; /* 내부 여백만 유지 */
    background-color: transparent;
    box-sizing: border-box;
}
.main-title { font-size: 2rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.5px; }
.sub-title { color: #6A7683; margin: 8px 0 0 0; font-weight: 500; font-size: 0.9rem; }

/* 메인 콘텐츠 영역 (고정 해제에 따른 여백 조정) */
.main-content { 
    width: 100%;
    display: flex; flex-direction: column; gap: 50px; 
}

/* 월 섹션 구조 */
.month-section { 
    display: grid; 
    grid-template-columns: 100px 1fr; 
    gap: 30px; 
    align-items: start; 
}

/* 월 레이블 (카드를 따라가도록 고정 위치는 유지) */
.month-sidebar { 
    position: sticky; top: 20px; 
    background-color: #FFFFFF; color: #1A1A1A; 
    padding: 12px; border-radius: 14px; 
    font-weight: 800; font-size: 1.1rem; text-align: center; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
}

/* 프로젝트 리스트 */
.project-list { 
    display: grid; 
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
    gap: 16px; 
    align-items: start; 
}

/* 카드 디자인 */
.project-card { 
    background-color: #FFFFFF !important; 
    border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); 
    box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
    overflow: hidden; transition: transform 0.2s ease, box-shadow 0.2s ease; 
}
.project-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }

summary { list-style: none; padding: 20px 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; outline: none; }
summary::-webkit-details-marker { display: none; }
.card-project-title { font-size: 1.15rem; font-weight: 800; color: #1A1A1A; margin: 0; }
.card-content { padding: 0 24px 24px 24px; }
.card-desc { font-size: 0.9rem; line-height: 1.6; margin: 10px 0; color: #333; font-weight: 500; }
.card-manager { font-size: 0.8rem; color: #1A1A1A; opacity: 0.7; margin: 0; font-weight: 400; }
.arrow-icon { width: 8px; height: 8px; border-top: 2.5px solid #BCB8AD; border-right: 2.5px solid #BCB8AD; transform: rotate(135deg); transition: transform 0.3s ease; }
details[open] .arrow-icon { transform: rotate(-45deg); border-color: #1A1A1A; }
.badge-wrapper { display: flex; gap: 4px; margin-top: 8px; }
.badge { padding: 4px 12px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; }
</style>""", unsafe_allow_html=True)

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

# 4. 상단 헤더 (포지션 고정 해제됨)
st.markdown('<div class="static-header"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>', unsafe_allow_html=True)

# 5. 메인 콘텐츠 (월별 섹션)
if not df.empty:
    html_buffer = ['<div class="main-content">']
    for m in range(1, 7):
        month_tasks = df[df['StartMonth'] == m]
        html_buffer.append(f'<div class="month-section"><div class="month-sidebar">{m}월</div><div class="project-list">')
        if not month_tasks.empty:
            for _, row in month_tasks.iterrows():
                cat = str(row['Category']).strip()
                status = str(row['Status']).strip()
                theme = COLOR_PALETTE.get(cat, COLOR_PALETTE["Default"])
                badge_html = f'<div class="badge-wrapper"><div class="badge" style="background-color: {theme["main"]}15; color: {theme["main"]}; border: 1.5px solid {theme["main"]}30;">{cat} {status}</div></div>'
                card_html = (
                    f'<details class="project-card"><summary><div>'
                    f'<div class="card-project-title">{row["Project"]}</div>{badge_html}</div>'
                    f'<div class="arrow-icon"></div></summary>'
                    f'<div class="card-content"><div class="card-desc">{row["Description"]}</div>'
                    f'<div class="card-manager">{row["Manager"]}</div></div></details>'
                )
                html_buffer.append(card_html)
        else:
            html_buffer.append('<div style="color: #BCB8AD; font-style: italic; font-size: 0.85rem; padding-top: 15px;">예정된 프로젝트 없음</div>')
        html_buffer.append('</div></div>')
    html_buffer.append('</div>')
    st.markdown("".join(html_buffer).replace("\n", ""), unsafe_allow_html=True)
