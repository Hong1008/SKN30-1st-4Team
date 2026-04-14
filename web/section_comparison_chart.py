import streamlit as st
import plotly.express as px

def section_comparison_chart(df):
    """수요-공급 비교 바 차트를 렌더링합니다."""
    st.markdown("---")
    st.subheader("📈 수요-공급 비교 분석")

    top_10 = df.sort_values('불편_지수', ascending=False).head(10)
    chart_data = top_10[['시도', '전기차_등록수', '충전기_대수', '불편_지수']]

    fig = px.bar(
        chart_data,
        x='시도',
        y=['전기차_등록수', '충전기_대수'],
        barmode='group',
        title='상위 10개 지역: 전기차 등록수 vs 충전기 수',
        color_discrete_map={'전기차_등록수': 'blue', '충전기_대수': 'orange'},
        labels={'value': '대수', 'variable': '구분'}
    )

    for _, row in chart_data.iterrows():
        fig.add_annotation(
            x=row['시도'], y=row['전기차_등록수'],
            text=f"불편: {row['불편_지수']:.0f}",
            showarrow=True, arrowhead=1, yshift=10
        )

    st.plotly_chart(fig, width='stretch')
