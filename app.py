import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 로드맵", layout="wide", initial_sidebar_state="collapsed")

# 구글 시트 연동
SHEET_ID = '1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA' 
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# 2. CSS 디자인 (가로 스패닝 및 텍스트 스타일 수정)
st.markdown("""
<style>
    /* 배경 및 사이드바 제거 */
    [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #F2F5F8; }
    
    /* 제목 */
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1A1A1A; padding: 20px 0 5px 0; letter-spacing: -1.5px; }
    .sub-title { color: #6A7683; margin-bottom: 40px; font-weight: 500; font-size: 0.9rem; }

    /* 타임라인 그리드 시스템 */
    .timeline-wrapper {
        display: grid;
        grid-template-columns: repeat(6, 1fr); /* 6개월 등분 */
        gap: 20px;
        width: 100%;
    }

    /* 월 헤더 스타일 */
    .month-header {
        background-color: #FFFFFF;
        color: #1A1A1A;
        padding: 12px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        margin-bottom: 10px;
    }

    /* 프로젝트 카드 스타일 (흰색 박스 고정) */
    .project-card {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
        margin-bottom: 20px; /* 카드 간 간격 */
    }

    /* 텍스트 스타일 교체 반영 */
    .card-project-title { font-size: 1.1rem; font-weight: 800; margin-bottom: 6px; }
    .card-desc { font-size: 0.9rem; line-height: 1.4; margin-bottom: 15px; color: #1A1A1A; font-weight: 500; }
    
    /* 담당자 및 기간: 폰트 축소, Regular, 투명도 70% */
    .card-info-row { 
        font-size: 0.75rem; 
        font-weight: 400; 
        color: #1A1A1A; 
        opacity: 0.7; 
        margin-bottom: 15px; 
        display: flex; 
        justify-content: space-between; 
    }
    
    /* 뱃지 */
    .badge-wrapper { display: flex; g
