from web.view import show_data_by_year
from web.view import show_data_by_area
from domain.load_by_csv import load_ev
import streamlit as st

def main():

    st.set_page_config(
        page_title="전기차 충전 인프라 대시보드",
        page_icon="🔌",
        layout="wide"
    )
    df = st.cache_data(load_ev)()

    # 탭 생성
    tab1, tab2 = st.tabs(["연도별", "지역별"])

    with tab1:
        show_data_by_year(df)

    with tab2:
        show_data_by_area(df)


    # 푸터
    st.divider()
    st.caption("© SKN30-1st-4Team")

if __name__ == "__main__":
    main()
