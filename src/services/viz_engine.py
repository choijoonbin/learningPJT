import plotly.express as px
import plotly.graph_objects as go

class VisualizationEngine:
    @staticmethod
    def create_line_chart(df, x_col, y_col, title="Data Trend"):
        fig = px.line(df, x=x_col, y=y_col, title=title, template="plotly_white")
        fig.update_layout(hovermode="x unified")
        return fig

    @staticmethod
    def create_bar_chart(df, x_col, y_col, title="Category Distribution"):
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=y_col, color_continuous_scale="Viridis")
        return fig

    @staticmethod
    def create_heatmap(df, title="Feature Correlation"):
        corr = df.corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto", title=title, color_continuous_scale='RdBu_r')
        return fig