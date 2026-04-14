import streamlit as st
from domain.ev_service import load_ev_data, filter_data
from web.sidebar import render_sidebar
from web.section_map import section_map
from web.section_comparison_chart import section_comparison_chart
from web.section_data_table import section_data_table
from web.section_insights import section_insights

def sample_page():
    # 1. 앱 기본 설정
    st.set_page_config(
        page_title="전기차 충전 인프라 대시보드",
        page_icon="🔌",
        layout="wide"
    )

    # 2. 데이터 로드 (Service Layer)
    df = st.cache_data(load_ev_data)()

    # 3. 사이드바 및 필터 처리 (UI Component)
    selected_region, rank_range = render_sidebar(df)

    # 4. 데이터 필터링 (Service Layer)
    df_filtered = filter_data(df, selected_region, rank_range)

    # 5. 메인 컨텐츠 렌더링 (Main UI Components)
    # 1) SOS 핫스팟 히트맵
    section_map(df, df_filtered)

    # 2) 수요-공급 비교 차트
    section_comparison_chart(df)

    # 3) 상세 데이터 테이블
    section_data_table(df_filtered, selected_region)

    # 4) 인사이트 요약
    section_insights(df_filtered, selected_region)

if __name__ == "__main__":
    sample_page()
