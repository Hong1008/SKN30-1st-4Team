import pandas as pd
import streamlit as st
from domain.ev_schema import EVSchema


def section_data_table(df, selected_region, key="default"):
    """상세 데이터 테이블과 다운로드 버튼을 렌더링합니다."""
    
    st.markdown("---")

    if df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    df_filtered = df.sort_values(by=EVSchema.discomfort_index, ascending=False)
    df_filtered = df_filtered.drop(columns=[EVSchema.lat, EVSchema.lon], errors='ignore')

    if df_filtered.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    st.subheader("📋 상세 데이터 테이블")
    csv_data = df_filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv_data,
        file_name=f'ev_dashboard_{selected_region}_{pd.Timestamp.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        width='content',
        key=f'download_{key}'
    )

    st.dataframe(
        df_filtered,
        width="stretch",
        hide_index=True,
        column_config={
            EVSchema.discomfort_index: st.column_config.NumberColumn(
                "불편 지수", format="%.2f"
            ),
            EVSchema.ev_count: st.column_config.NumberColumn(
                "전기차 등록수", format="%d"
            ),
            EVSchema.charger_count: st.column_config.NumberColumn(
                "충전기 대수", format="%d"
            ),
        },
    )
