import plotly.express as px
import streamlit as st
import pandas as pd
from domain.ev_schema import EVSchema


def section_comparison_chart(df, idkey):
    """수요-공급 비교 바 차트를 렌더링합니다."""
    st.markdown("---")
    st.subheader("📈 수요-공급 비교 분석")

    # 컬럼이 연도이므로 가장 최근 연도 또는 단일 연도를 기준으로 데이터를 추출합니다.
    target_year = sorted(df.columns.tolist())[-1]
    
    # 선택된 연도의 데이터를 평탄화(Flat DataFrame)
    data_list = df[target_year].dropna().tolist()
    flat_df = pd.DataFrame(data_list)

    if flat_df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return


    top_10 = flat_df.sort_values(EVSchema.discomfort_index, ascending=False).head(10)
    chart_data = top_10[
        [
            EVSchema.region,
            EVSchema.ev_count,
            EVSchema.charger_count,
            EVSchema.discomfort_index,
        ]
    ]

    fig = px.bar(
        chart_data,
        x=EVSchema.region,
        y=[EVSchema.ev_count, EVSchema.charger_count],
        barmode="group",
        title="상위 10개 지역: 전기차 등록수 vs 충전기 수",
        color_discrete_map={
            EVSchema.ev_count: "blue",
            EVSchema.charger_count: "orange",
        },
        labels={"value": "대수", "variable": "구분"},
    )

    for _, row in chart_data.iterrows():
        fig.add_annotation(
            x=row[EVSchema.region],
            y=row[EVSchema.ev_count],
            text=f"불편: {row[EVSchema.discomfort_index]:.0f}",
            showarrow=True,
            arrowhead=1,
            yshift=10,
        )

    st.plotly_chart(fig, width='stretch', key=idkey)
