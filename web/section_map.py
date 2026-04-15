import folium
import pandas as pd
import streamlit as st
from domain.ev_schema import EVSchema
from streamlit_folium import st_folium


def section_map(df, selected_year):
    """SOS 핫스팟 히트맵을 렌더링합니다."""
    if selected_year == '전체':
        st.subheader("📍 SOS 핫스팟 히트맵")
    else:
        st.subheader(f"📍 {selected_year}년도 SOS 핫스팟 히트맵")
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        # tiles='CartoDB positron'
        tiles='OpenStreetMap'
    )

    if df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    # 컬럼이 연도이므로 가장 최근 연도 또는 단일 연도를 기준으로 데이터를 추출합니다.
    target_year = sorted(df.columns.tolist())[-1]

    # 선택된 연도의 데이터를 평탄화(Flat DataFrame)
    data_list = df[target_year].dropna().tolist()
    flat_df = pd.DataFrame(data_list)

    if flat_df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    min_val = flat_df[EVSchema.discomfort_index].min()
    max_val = flat_df[EVSchema.discomfort_index].max()

    for _, row in flat_df.iterrows():
        value = row.get(EVSchema.discomfort_index, 0)
        normalized = (value - min_val) / (max_val - min_val) if (max_val - min_val) > 0 else 0
        color = 'blue' if normalized < 0.33 else 'orange' if normalized < 0.66 else 'red'

        popup_html = f"""
        <div style="width: 200px;">
            <h4 style="margin-bottom: 5px;">{row[EVSchema.region]}</h4>
            <p style="margin: 2px 0;"><b>불편 지수:</b> {value:.2f}</p>
            <p style="margin: 2px 0;"><b>순위:</b> {row[EVSchema.discomfort_rank]}</p>
            <p style="margin: 2px 0;"><b>전기차 수:</b> {row[EVSchema.ev_count]:,}</p>
            <p style="margin: 2px 0;"><b>충전기 수:</b> {row[EVSchema.charger_count]:,}</p>
        </div>
        """

        folium.CircleMarker(
            location=[row[EVSchema.lat], row[EVSchema.lon]],
            radius=normalized * 30 + 5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_html, max_width=300),
        ).add_to(m)

    st_folium(m, use_container_width=True, height=600, key="main_map")
