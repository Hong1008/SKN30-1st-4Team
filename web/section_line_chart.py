import streamlit as st
from domain.ev_service import EVSchema


def section_line_chart(df):
    """지역별 전기차 등록수 및 충전기 대수 라인 차트를 렌더링합니다."""
    st.markdown("---")
    st.subheader("📈 지역별 전기차 · 충전기 현황")

    chart_df = (
        df[[EVSchema.region, EVSchema.ev_count, EVSchema.charger_count]]
        .set_index(EVSchema.region)
        .sort_values(EVSchema.ev_count, ascending=False)
        .rename(columns={
            EVSchema.ev_count: "전기차 등록수",
            EVSchema.charger_count: "충전기 대수",
        })
    )

    st.line_chart(chart_df)
