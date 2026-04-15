from web.view import show_data_by_year
from web.view import show_data_by_area
from domain.ev_service import load_ev_data
import streamlit as st

def main():

    st.set_page_config(
        page_title="전기차 충전 인프라 대시보드",
        page_icon="🔌",
        layout="wide"
    )
    df_year, df_region = st.cache_data(load_ev_data)()

    # 탭 생성
    tab1, tab2 = st.tabs(["연도별", "지역별"])

    with tab1:
        show_data_by_year(df_year)

    with tab2:
        show_data_by_area(df_region)


    # 푸터
    st.divider()
    st.caption("© SKN30-1st-4Team")

if __name__ == "__main__":
    main()
