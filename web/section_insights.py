import streamlit as st
from domain.ev_schema import EVSchema
import pandas as pd



def section_insights(df, selected_region):
    """주요 인사이트 요약을 렌더링합니다."""
    st.markdown("---")
    st.subheader("💡 주요 인사이트")

    if df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    # 평탄화
    data_list = []
    for col in df.columns:
        for val in df[col].dropna().tolist():
            if isinstance(val, dict):
                data_list.append(val)
                
    flat_df = pd.DataFrame(data_list)

    if flat_df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    # 값이 있는 경우, 불편 지수가 가장 높은 행(가장 심각한 지역) 추출
    top_problem = flat_df.sort_values(EVSchema.discomfort_index, ascending=False).iloc[0]
    region_name = top_problem.get(EVSchema.region, "알수없음")
    discomfort = top_problem.get(EVSchema.discomfort_index, 0)
    ev_count = top_problem.get(EVSchema.ev_count, 0)
    charger_count = top_problem.get(EVSchema.charger_count, 0)

    # 심각도 분류
    status = "심각(높음)" if discomfort >= 3.0 else "주의(보통)" if discomfort >= 1.5 else "양호(낮음)"

    st.markdown(f"### 🚨 {region_name} 지역 집중 인프라 확충 필요")
    st.markdown(
        f"- **불편 지수**: {discomfort:.2f} ({status}) - 충전기 1대당 감당하는 전기차 수"
    )
    st.markdown(
        f"- **현재 인프라 상태**: 전기차 {ev_count:,}대 / 충전기 {charger_count:,}대"
    )
    
    # 목표 불편 지수(예: 1.5대 당 1대 만족)를 맞추기 위한 추가 필요 충전기 수 
    ideal_chargers = int(ev_count / 1.5)
    needed = ideal_chargers - charger_count if ideal_chargers > charger_count else 0
    
    if needed > 0:
        st.markdown(
            f"- **해결 방안**: 평균적인 충전 쾌적성을 위해 최소 **{needed:,}대**의 충전기 추가 설치 검토 필요"
        )
    else:
        st.markdown("- **해결 방안**: 현재 인프라가 상대적으로 양호하게 구축되어 있습니다.")
