import streamlit as st
from src.services.agent_logic import AnalysisAgent

def render_chat_page():
    st.header("💬 AI Data Agent")

    # 세션 상태에 채팅 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 데이터가 로드되어 있는지 확인
    if "data" not in st.session_state:
        st.warning("먼저 'Data Analysis' 메뉴에서 파일을 업로드해 주세요.")
        return

    # 대화 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("데이터에 대해 궁금한 점을 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            agent = AnalysisAgent(st.session_state.data)
            response = agent.ask(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})