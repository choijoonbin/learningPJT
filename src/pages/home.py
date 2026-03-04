import streamlit as st
from src.utils.stats import get_data_summary

def render_home_page():
    st.title("🏠 AuraAgent Dashboard")
    
    if "data" not in st.session_state:
        st.info("데이터가 아직 로드되지 않았습니다. Analysis 메뉴에서 파일을 업로드해 주세요.")
        # 사이트 느낌의 Placeholder 카드들
        col1, col2, col3 = st.columns(3)
        col1.metric("Status", "Waiting...", delta="0")
        col2.metric("Records", "0", delta="0")
        col3.metric("Features", "0", delta="0")
    else:
        df = st.session_state.data
        summary = get_data_summary(df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("총 레코드", f"{summary['total_rows']:,}", "Rows")
        col2.metric("컬럼 수", f"{summary['total_cols']}", "Features")
        col3.metric("결측치", f"{summary['missing_values']}", "Nulls", delta_color="inverse")
        col4.metric("수치형 변수", f"{summary['numeric_cols']}", "Numeric")
        
        st.divider()
        st.subheader("Quick Data Insight")
        st.write("최근 업로드된 데이터의 기술 통계량입니다.")
        st.dataframe(df.describe().T, use_container_width=True)