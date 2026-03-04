import streamlit as st
from src.components.sidebar import render_sidebar
from src.constants import settings

def main():
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        page_icon=settings.PAGE_ICON,
        layout=settings.LAYOUT
    )

    # 사이드바 렌더링
    selected_menu = render_sidebar()

    # 메인 화면 로직 (메뉴 선택에 따른 분기)
    if selected_menu == "Home":
        st.title("Welcome to AI Agent Dashboard")
        st.write("분석할 데이터를 업로드하거나 에이전트와 대화를 시작하세요.")
    elif selected_menu == "Data Analysis":
        # 추후 구현 예정
        pass

if __name__ == "__main__":
    main()