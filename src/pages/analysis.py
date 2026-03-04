import streamlit as st
import pandas as pd
from src.services.viz_engine import VisualizationEngine

def render_analysis_page():
    st.header("📊 Data Analysis Dashboard")
    
    uploaded_file = st.file_uploader("분석할 CSV 파일을 업로드하세요", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        col1, col2 = st.columns(2)
        viz = VisualizationEngine()
        
        with col1:
            # 수치형 컬럼 자동 추출
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if num_cols:
                target_col = st.selectbox("시계열 분석 대상 선택", num_cols)
                fig = viz.create_line_chart(df, df.index, target_col)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if len(num_cols) >= 2:
                fig_heat = viz.create_heatmap(df[num_cols])
                st.plotly_chart(fig_heat, use_container_width=True)