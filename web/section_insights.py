import streamlit as st
from domain.ev_schema import EVSchema


def section_insights(df_filtered, selected_region):
    """주요 인사이트 요약을 렌더링합니다."""
    st.markdown("---")
    st.subheader("💡 주요 인사이트")

    if not df_filtered.empty:
        region_data = df_filtered.iloc[0]
        st.markdown(f"### {selected_region} 지역 분석")
        st.markdown(
            f"- **불편 지수**: {region_data[EVSchema.discomfort_index]:.2f} (높음/보통/낮음)"
        )
        st.markdown(
            f"- **전기차 밀도**: 인구 1만 명당 {region_data[EVSchema.demand_density]:.1f}대"
        )
        st.markdown(
            f"- **충전기 밀도**: 면적 100km²당 {region_data[EVSchema.supply_density]:.1f}대"
        )
        st.markdown(
            f"- **해결 방안**: {region_data[EVSchema.charger_count]:,}대의 충전기 추가 설치 필요"
        )
    else:
        st.markdown("- 데이터가 없습니다.")
