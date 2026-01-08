import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="한빛앤 프로덕트 로드맵", layout="wide")

# 2. 커스텀 CSS (이미지와 동일한 스타일링)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #f8f9fa;
    }
    
    .main-title {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 5px;
        color: #1e1e1e;
    }
    
    .sub-title {
        font-size: 16px;
        color: #6c757d;
        margin-bottom: 30px;
    }

    /* 타임라인 그리드 레이아웃 */
    .timeline-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 20px;
        margin-top: 20px;
    }

    .month-header {
        background: white;
        padding: 10px;
        text-align: center;
        border-radius: 12px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 로드맵 카드 스타일 */
    .project-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        position: relative;
        transition: transform 0.2s;
    }
    
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }

    .project-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
        color: #212529;
    }

    /* 상태 배지 스타일 */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-qa { background-color: #e6f9f0; color: #17a05e; }        /* QA 진행중: 초록 */
    .status-dev { background-color: #e7f3ff; color: #007bff; }       /* 개발 진행중: 파랑 */
    .status-plan { background-color: #f1f3f5; color: #495057; }      /* 논의 예정: 회색 */
    .status-ready { background-color: #fff9db; color: #f08c00; }     /* 개발 예정: 주황/노랑 */

    /* 화살표 아이콘 대체 (카드 오른쪽 끝) */
    .arrow {
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        color: #dee2e6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드 함수
def load_data():
    sheet_id = "1Z3n4mH5dbCgv3RhSn76hqxwad6K60FyEYXD_ns9aWaA"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        # 테스트용 더미 데이터 (시트 접근 안될 경우)
        data = {
            'Project': ['주문/결제 개편', '뷰어 개편', 'HA+ 디지털교재', '교강사 전자책 증정', '한빛+ App 런칭', '마이한빛 개편'],
            'StartMonth': [1, 1, 1, 1, 1, 1],
            'EndMonth': [1, 1, 3, 1, 3, 3],
            'Status 1': ['QA 진행중', '개발 진행중', '개발 예정', '개발 진행중', '개발 진행중', '논의 예정']
        }
        return pd.DataFrame(data)

df = load_data()

# 4. 헤더 렌더링
st.markdown('<div class="main-title">한빛앤 프로덕트 로드맵</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 상반기 마일스톤 타임라인</div>', unsafe_allow_html=True)

# 5. 월별 헤더 (1월~6월)
cols = st.columns(6)
months = ["1월", "2월", "3월", "4월", "5월", "6월"]
for i, month in enumerate(months):
    cols[i].markdown(f'<div class="month-header">{month}</div>', unsafe_allow_html=True)

# 6. 로드맵 본문 렌더링
# CSS Grid를 활용하여 프로젝트 카드가 여러 컬럼을 차지하도록 구현
for _, row in df.iterrows():
    # 상태별 클래스 지정
    status_class = "status-plan"
    status_text = row['Status 1']
    
    if "QA" in status_text: status_class = "status-qa"
    elif "개발 진행" in status_text: status_class = "status-dev"
    elif "개발 예정" in status_text: status_class = "status-ready"
    
    # 시작월과 종료월 계산 (1~6)
    start = int(row['StartMonth'])
    end = int(row['EndMonth'])
    span = end - start + 1
    
    # Streamlit 컬럼 시스템을 활용한 배치
    # 시작 위치에 맞춰 빈 공간(empty columns)을 만들거나, 
    # HTML Grid를 직접 사용하여 더 정확한 레이아웃 구현
    
    grid_html = f"""
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 20px; margin-bottom: 15px;">
        <div style="grid-column: {start} / span {span};">
            <div class="project-card">
                <div class="project-title">{row['Project']}</div>
                <div class="badge {status_class}">{status_text}</div>
                <div class="arrow">❯</div>
            </div>
        </div>
    </div>
    """
    st.markdown(grid_html, unsafe_allow_html=True)

# 7. 푸터 관리자 모드
st.sidebar.markdown("### 대시보드 관리")
if st.sidebar.button("데이터 새로고침"):
    st.rerun()
