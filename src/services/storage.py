import os
import pandas as pd
import streamlit as st

class StorageService:
    @staticmethod
    def save_uploaded_file(uploaded_file):
        if not os.path.exists("data"):
            os.makedirs("data")
        
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 세션에 데이터프레임 로드
        st.session_state.data = pd.read_csv(file_path)
        st.session_state.file_name = uploaded_file.name
        return file_path