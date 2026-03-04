import streamlit as st
from src.utils.monitor import get_system_info

def render_sidebar():
    with st.sidebar:
        st.title("🚀 AuraAgent System")
        
        # 메뉴 선택
        menu = st.radio("Navigation", ["Home", "Data Analysis", "Chat Agent", "System Status"])
        
        st.divider()
        
        # 시스템 모니터링 섹션 (사이트 동일 구성)
        st.subheader("System Monitor")
        sys_info = get_system_info()
        st.metric("CPU Usage", f"{sys_info['cpu_usage']}%")
        st.metric("Memory Usage", f"{sys_info['memory_usage']}%")
        st.caption(f"Last Update: {sys_info['last_sync']}")
        
        return menu