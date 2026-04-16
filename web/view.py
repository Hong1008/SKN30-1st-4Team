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

    left, center, right = st.columns([2,0.2,3], vertical_alignment='top')
    with left:
        section_map(df_filtered, selected_year)

    with center:
        pass
    with right:
        # 통계 카드 스타일
        st.markdown("""
        <style>
        .stat-card {
            border: 1.5px solid #d0d0d0;
            border-radius: 10px;
            padding: 16px 12px 12px 12px;
            text-align: center;
            background: #fafafa;
            margin-bottom: 8px;
        }
        .stat-label {
            font-size: 13px;
            color: #888;
            margin-bottom: 4px;
        }
        .stat-region {
            font-size: 20px;
            font-weight: 700;
            color: #222;
        }
        .stat-value {
            font-size: 14px;
            color: #555;
            margin-top: 2px;
        }
        .emoji-icon {
            font-size: 16px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.subheader('')
        left1, center1, right1 = st.columns([1, 1, 1])

        top_ev = df_filtered.loc[df_filtered[EVSchema.ev_count].idxmax()]
        top_charger = df_filtered.loc[df_filtered[EVSchema.charger_count].idxmax()]
        top_discomfort = df_filtered.loc[df_filtered[EVSchema.discomfort_index].idxmax()]

        with left1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label"><span class="emoji-icon"> 🏆 </span> 전기차 최다 지역</div>
                <div class="stat-label"><span class="emoji-icon">🏆</span> 전기차 최다 지역</div>
                <div class="stat-region">{top_ev[EVSchema.region]}</div>
                <div class="stat-value">{int(top_ev[EVSchema.ev_count]):,} 대</div>
            </div>
            """, unsafe_allow_html=True)

        with center1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label"><span class="emoji-icon">⭐</span> 충전기 최다 지역</div>
                <div class="stat-region">{top_charger[EVSchema.region]}</div>
                <div class="stat-value">{int(top_charger[EVSchema.charger_count]):,} 기</div>
            </div>
            """, unsafe_allow_html=True)

        with right1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label"><span class="emoji-icon">🔥</span> 불편지수 최고 지역</div>
                <div class="stat-region">{top_discomfort[EVSchema.region]}</div>
                <div class="stat-value">지수 {top_discomfort[EVSchema.discomfort_index]:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

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
