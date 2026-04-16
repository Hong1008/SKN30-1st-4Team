import streamlit as st
from web.section_map import section_map
from web.section_data_table import section_data_table
from web.section_comparison_chart import section_comparison_chart
from web.section_line_chart import section_line_chart
from web.section_wordcloud import section_wordcloud
from domain.ev_schema import EVSchema

def show_data_by_year(df):
    years = sorted(df[EVSchema.year].astype(str).unique().tolist(), reverse=True)
    selected_year = st.segmented_control(
        "연도 선택",
        options=years,
        default=years[0],
        label_visibility="collapsed",
        key="year_selector"
    )

    # 선택된 연도로 필터링
    df_filtered = df[df[EVSchema.year].astype(str) == selected_year]

    left, center, right = st.columns([2,0.2,3], vertical_alignment='center')
    with left:
        section_map(df_filtered, selected_year)

    with center:
        pass
    with right:

        # 필터 / 데이터 영역
        # st.subheader("필터")
        # st.write("여기에 필터 및 데이터 내용을 추가하세요.")

        # st.markdown("---")

        # 워드 클라우드 자리
        section_wordcloud(selected_year)



    section_comparison_chart(df_filtered, 'chart_year')

    # 상세 테이블
    section_data_table(df_filtered, '전체', key='year')

def show_data_by_area(df):
    areas = sorted(df[EVSchema.region].unique().tolist())
    selected_area = st.segmented_control(
        "지역 선택",
        options=areas,
        default=areas[0],
        label_visibility="collapsed",
        key="area_selector"
    )

    # 선택된 지역으로 필터링
    df_filtered = df[df[EVSchema.region] == selected_area]

    # 라인 테이블
    section_line_chart(df_filtered)

    # 상세 테이블
    section_data_table(df_filtered, '전체', key='area')
