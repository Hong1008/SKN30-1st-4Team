import streamlit as st
from domain.ev_service import EVSchema
import pandas as pd


def section_line_chart(df):
    """지역별 전기차 등록수 및 충전기 대수 라인 차트를 렌더링합니다."""
    st.markdown("---")
    st.subheader("📈 통계 추이 현황")

    if df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    # 제공된 DataFrame(연도/지역의 딕셔너리 구조)을 평탄화(Flat) 합니다.
    data_list = []
    for col in df.columns:
        for val in df[col].dropna().tolist():
            if isinstance(val, dict):
                data_list.append(val)
                
    flat_df = pd.DataFrame(data_list)

    if flat_df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return
    
    # x축을 무엇으로 할지 결정 (데이터에 여러 연도가 있으면 연도별 트렌드를, 여러 지역만 있으면 지역별 비교를 수행)
    unique_years = flat_df[EVSchema.year].nunique()
    unique_regions = flat_df[EVSchema.region].nunique()

    if unique_years > 1 and unique_regions == 1:
        # 특정 한 지역의 여러 연도 데이터 -> 연도별 추이(라인 차트)
        chart_df = (
            flat_df[[EVSchema.year, EVSchema.ev_count, EVSchema.charger_count]]
            .groupby(EVSchema.year)
            .sum()
        )
    else:
        # 특정 연도의 여러 지역 데이터 (또는 전체 데이터) -> 지역별 비교
        chart_df = (
            flat_df[[EVSchema.region, EVSchema.ev_count, EVSchema.charger_count]]
            .groupby(EVSchema.region)
            .sum()
            .sort_values(EVSchema.ev_count, ascending=False)

        )

    st.line_chart(chart_df)
