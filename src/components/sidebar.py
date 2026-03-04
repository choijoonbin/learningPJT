import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.image("assets/logo.png") # 로고 파일 필요 시 대체
        st.title("Menu")
        
        menu = st.radio(
            "Navigation",
            ["Home", "Data Analysis", "Chat Agent", "Settings"]
        )
        
        st.divider()
        st.info("Agent Status: Online")
        
        return menu