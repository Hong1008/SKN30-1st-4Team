import streamlit as st
from web.section_map import section_map
from web.section_data_table import section_data_table
from web.section_comparison_chart import section_comparison_chart
from web.section_line_chart import section_line_chart

def show_data_by_year(df, df_filtered):

    selected_year = st.segmented_control(
        "연도 선택",
        options=["전체"] + list(range(2018, 2027)),
        default="전체",
        label_visibility="collapsed",
        key="year_selector"
    )


    left, center, right = st.columns([2,0.2,3])
    with left:
        section_map(df, df_filtered)

    with center:
        pass
    with right:

        # 필터 / 데이터 영역
        st.subheader("필터")
        st.write("여기에 필터 및 데이터 내용을 추가하세요.")

        st.markdown("---")

        # 워드 클라우드 자리
        st.subheader("워드 클라우드")
        st.markdown(
            "<div style='height:300px; display:flex; align-items:center; justify-content:center;"
            " border:2px dashed #aaa; border-radius:8px; color:#aaa;'>워드 클라우드 이미지 자리</div>",
            unsafe_allow_html=True
        )


    section_comparison_chart(df, 'chart_year')

    # 상세 테이블
    section_data_table(df_filtered, '전체', key='year')

def show_data_by_area(df, df_filtered):
    selected_area = st.segmented_control(
        "지역 선택",
        options=['전체','서울'],
        default='전체',
        label_visibility="collapsed",
        key="area_selector"
    )

    # 라인 테이블
    section_line_chart(df)

    # 상세 테이블
    section_data_table(df_filtered, '전체', key='area')
