import streamlit as st
import pandas as pd

def section_data_table(df_filtered, selected_region):
    """상세 데이터 테이블과 다운로드 버튼을 렌더링합니다."""
    st.markdown("---")
    
    st.subheader("📋 상세 데이터 테이블")
    csv_data = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv_data,
        file_name=f'ev_dashboard_{selected_region}_{pd.Timestamp.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        width='content'
    )

    st.dataframe(
        df_filtered,
        width='stretch',
        hide_index=True,
        column_config={
            "불편_지수": st.column_config.NumberColumn("불편 지수", format="%.2f"),
            "전기차_등록수": st.column_config.NumberColumn("전기차 등록수", format="%d"),
            "충전기_대수": st.column_config.NumberColumn("충전기 대수", format="%d"),
        }
    )
