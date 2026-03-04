import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import os

class AnalysisAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # 사이트에서 사용하는 스마트한 분석을 위해 gpt-4o 또는 gpt-3.5-turbo 설정
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o")
        self.agent = create_pandas_dataframe_agent(
            self.llm, 
            self.df, 
            verbose=True, 
            allow_dangerous_code=True # 데이터 분석 코드 실행 허용
        )

    def ask(self, query: str):
        try:
            response = self.agent.run(query)
            return response
        except Exception as e:
            return f"분석 중 오류가 발생했습니다: {str(e)}"