import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 페이지 설정 및 디자인 (화이트 배경 + 알록달록 카드)
st.set_page_config(page_title="Project Scheduler", layout="wide")

SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# CSS: 화이트 배경과 알록달록한 카드 스타일링
st.markdown("""
    <style>
    /* 전체 배경을 흰색으로 */
    .stApp {
        background-color: #FFFFFF;
    }
    /* 사이드바 - 다크 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* 캘린더 카드 공통 스타일 */
    .calendar-card {
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: none;
        transition: transform 0.2s;
    }
    .calendar-card:hover {
        transform: translateY(-3px);
    }
    .card-time {
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 8px;
        opacity: 0.8;
    }
    .card-project {
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .card-title {
        font-weight: 700;
        font-size: 1.05rem;
        line-height: 1.3;
        margin-bottom: 10px;
    }
    /* 요일 헤더 */
    .day-header {
        text-align: center;
        padding: 15px 0;
        margin-bottom: 20px;
        border-radius: 12px;
    }
    .day-name { font-size: 0.7rem; font-weight: 700; color: #999; }
    .day-date { font-size: 1.2rem; font-weight: 800; color: #222; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 로드 함수
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

# 카테고리별 색상 매핑 (이미지의 파스텔/비비드 톤)
COLOR_MAP = {
    "Design": {"bg": "#FFE5F1", "text": "#FF3DAB"},   # 핑크
    "Dev": {"bg": "#E5F0FF", "text": "#007AFF"},      # 블루
    "Planning": {"bg": "#FFF4D1", "text": "#FFAB00"}, # 옐로우
    "Meeting": {"bg": "#E8F9EE", "text": "#00C752"},  # 그린
    "Urgent": {"bg": "#F4EEFF", "text": "#7000FF"}    # 퍼플
}

try:
    df = load_data()
    
    # 사이드바
    st.sidebar.markdown("<h2 style='color:white;'>intelly</h2>", unsafe_allow_html=True)
    st.sidebar.write("")
    menu = st.sidebar.radio("Menu", ["📊 Dashboard", "📅 Schedule", "📋 Projects"])
    st.sidebar.markdown("---")
    all_projects = df['Project'].unique()
    selected_projects = st.sidebar.multiselect("Filter Projects", all_projects, default=all_projects)

    # 헤더
    st.markdown(f"<h1 style='color:#111; font-size:2.5rem;'>Stay up to date, Admin</h1>", unsafe_allow_html=True)
    
    # 상단 날짜 선택 (이번 주 기준)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    
    # 주간 레이아웃 (5컬럼)
    cols = st.columns(5)
    day_labels = ["MON", "TUE", "WED", "THU", "FRI"]

    for i in range(5):
        target_date = start_of_week + timedelta(days=i)
        with cols[i]:
            # 오늘 날짜 강조
            bg_style = "background-color: #000; color: #fff;" if target_date == today else "background-color: transparent;"
            date_color = "color: #fff;" if target_date == today else "color: #222;"
            
            st.markdown(f"""
                <div class="day-header" style="{bg_style}">
                    <div class="day-name">{day_labels[i]}</div>
                    <div class="day-date" style="{date_color}">{target_date.strftime('%d/%m')}</div>
                </div>
            """, unsafe_allow_html=True)

            # 해당 날짜 업무 필터링
            day_tasks = df[(df['Date'] == target_date) & (df['Project'].isin(selected_projects))]
            
            for _, row in day_tasks.iterrows():
                # 색상 결정
                style = COLOR_MAP.get(row['Category'], {"bg": "#F0F0F0", "text": "#444"})
                
                st.markdown(f"""
                    <div class="calendar-card" style="background-color: {style['bg']};">
                        <div class="card-time" style="color: {style['text']};">{row['Time']}</div>
                        <div class="card-project" style="color: {style['text']};">{row['Project']}</div>
                        <div class="card-title" style="color: #222;">{row['Task']}</div>
                        <div style="font-size: 0.7rem; font-weight: 600; color: {style['text']};">● {row['Status']}</div>
                    </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error("데이터 로딩 실패. 구글 시트 공유 설정과 컬럼명(Project, Task, Date, Time, Category, Status)을 확인하세요.")
