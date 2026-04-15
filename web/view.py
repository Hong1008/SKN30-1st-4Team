import streamlit as st
from web.section_map import section_map
from web.section_data_table import section_data_table
from web.section_comparison_chart import section_comparison_chart
from web.section_line_chart import section_line_chart
from web.section_wordcloud import section_wordcloud
from domain.ev_service import load_ev_data, filter_data

def show_data_by_year():

    selected_year = st.segmented_control(
        "연도 선택",
        options=["전체"] + list(range(2018, 2027)),
        default="전체",
        label_visibility="collapsed",
        key="year_selector"
    )


    df = st.cache_data(load_ev_data)()
    df_filtered = filter_data(df, selected_year, (1,2))

    left, center, right = st.columns([2,0.2,3])
    with left:
        section_map(df, df_filtered, selected_year)

    with center:
        pass

    with right:

        # 필터 / 데이터 영역
        st.subheader("필터")
        st.write("여기에 필터 및 데이터 내용을 추가하세요.")

        st.markdown("---")

        # 워드 클라우드 자리
        section_wordcloud(selected_year)

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

    df = st.cache_data(load_ev_data)()
    df_filtered = filter_data(df, selected_area, (1,2))
    # 라인 테이블
    section_line_chart(df)

    # 상세 테이블
    section_data_table(df_filtered, '전체', key='area')
