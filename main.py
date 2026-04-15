from web.view import show_data_by_year
from web.view import show_data_by_area
import streamlit as st

def main():

    st.set_page_config(
        page_title="전기차 충전 인프라 대시보드",
        page_icon="🔌",
        layout="wide"
    )

    # 탭 스타일 커스텀
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab"] {
            padding: 16px 32px;
        }
        .stTabs [data-baseweb="tab"] p {
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 탭 생성
    tab1, tab2 = st.tabs(["연도별", "지역별"])

    with tab1:
        show_data_by_year()

    with tab2:
        show_data_by_area()


    # 푸터
    st.divider()
    st.caption("© SKN30-1st-4Team")

if __name__ == "__main__":
    main()
