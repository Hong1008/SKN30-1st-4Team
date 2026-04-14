import streamlit as st
import folium
from streamlit_folium import st_folium

def section_map(df, df_filtered):
    """SOS 핫스팟 히트맵을 렌더링합니다."""
    st.subheader("📍 SOS 핫스팟 히트맵")
    
    m = folium.Map(
        location=[36.5, 127.5], 
        zoom_start=7,
        tiles='CartoDB positron'
    )

    if df_filtered.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
    else:
        min_val = df['불편_지수'].min()
        max_val = df['불편_지수'].max()
        
        for _, row in df_filtered.iterrows():
            value = row.get('불편_지수', 0)
            normalized = (value - min_val) / (max_val - min_val) if (max_val - min_val) > 0 else 0
            color = 'blue' if normalized < 0.33 else 'orange' if normalized < 0.66 else 'red'
            
            popup_html = f"""
            <div style="width: 200px;">
                <h4 style="margin-bottom: 5px;">{row['시도']}</h4>
                <p style="margin: 2px 0;"><b>불편 지수:</b> {value:.2f}</p>
                <p style="margin: 2px 0;"><b>순위:</b> {row['불편_순위']}</p>
                <p style="margin: 2px 0;"><b>전기차 수:</b> {row['전기차_등록수']:,}</p>
                <p style="margin: 2px 0;"><b>충전기 수:</b> {row['충전기_대수']:,}</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['위도'], row['경도']],
                radius=normalized * 30 + 5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(m)
        
        st_folium(m, width=1200, height=600, key="main_map")
