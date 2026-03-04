import streamlit as st
from src.components.sidebar import render_sidebar
from src.pages.home import render_home_page
from src.pages.analysis import render_analysis_page
from src.pages.chat import render_chat_page

def main():
    # 스타일 적용 (이전에 만든 CSS 로드)
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    selected_menu = render_sidebar()

    if selected_menu == "Home":
        render_home_page()
    elif selected_menu == "Data Analysis":
        render_analysis_page()
    elif selected_menu == "Chat Agent":
        render_chat_page()
    elif selected_menu == "System Status":
        st.header("🖥️ System Infrastructure")
        st.write("현재 AuraAgent가 작동 중인 서버 리소스 현황입니다.")
        # sidebar에서 이미 모니터링 중이므로 상세 내용 추가 가능

if __name__ == "__main__":
    main()