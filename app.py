import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. 디자인 CSS (코드 노출 방지를 위해 줄바꿈 최소화)
st.markdown("""<style>
header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
.stApp { background-color: #F2F5F8 !important; }
.sticky-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background-color: rgba(242, 245, 248, 0.85); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); padding: 30px 60px 20px 60px; box-sizing: border-box; }
.main-title { font-size: 1.8rem; font-weight: 800; color: #1A1A1A; margin: 0; letter-spacing: -1.2px; }
.sub-title { color: #6A7683; margin: 5px 0 0 0; font-weight: 500; font-size: 0.85rem; }
.main-content { margin-top: 130px; padding: 0 60px 60px 60px; display: flex; flex-direction: column; gap: 40px; }
.month-section { display: grid; grid-template-columns: 100px 1fr; gap: 30px; align-items: start; }
.month-sidebar { position: sticky; top: 140px; background-color: #FFFFFF; color: #1A1A1A; padding: 12px; border-radius: 14px; font-weight: 800; font-size: 1.1rem; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.project-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.project-card { background-color: #FFFFFF !important; border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 2px 8px rgba(0,0,0,0.02); overflow: hidden; transition: transform 0.2s ease; margin-bottom: 0px; }
.project-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }
summary { list-style: none; padding: 20px 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; outline: none; }
summary::-webkit-details-marker { display: none; }
.card-project-title { font-size: 1.1rem; font-weight: 800; color: #1A1A1A; margin: 0; }
.card-content { padding: 0 24px 24px 24px; }
.card-desc { font-size: 0.85rem; line-height: 1.6; margin: 10px 0; color: #333; font-weight: 500; }
.card-manager { font-size: 0.75rem; color: #1A1A1A; opacity: 0.7; font-weight: 400; margin: 0; }
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

# 4. 상단 고정 헤더
st.markdown('<div class="sticky-header"><div class="main-title">한빛앤 프로덕트 로드맵</div><div class="sub-title">2026 상반기 마일스톤 타임라인</div></div>', unsafe_allow_html=True)

# 5. 메인 콘텐츠 (월별 섹션 빌드)
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
    
    # 리스트를 하나의 문자열로 합치고 줄바꿈 제거 후 단 한 번만 렌더링
    st.markdown("".join(html_buffer).replace("\n", ""), unsafe_allow_html=True)
else:
    st.markdown('<div class="main-content">데이터 로딩 중...</div>', unsafe_allow_html=True)
