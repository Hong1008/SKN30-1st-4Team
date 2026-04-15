import streamlit as st
from domain.ev_service import EVSchema

def render_sidebar(df):
    """
    사용자 인터랙션을 위한 사이드바 UI를 렌더링합니다.
    데이터 현황 요약 스탯을 표시하고, 지역 및 순위 필터를 제공합니다.

    Args:
        df (pd.DataFrame): 대시보드에서 사용되는 전체 데이터프레임

    Returns:
        tuple: (selected_region, rank_range)
            - selected_region (str): 사용자가 드롭다운에서 선택한 지역명
            - rank_range (tuple): 사용자가 슬라이더에서 선택한 불편 순위 범위 (시작, 끝)
    """
    with st.sidebar:
        st.title("🔌 대시보드")
        st.markdown("---")
        
        st.subheader("📊 데이터 개요")
        st.metric("전체 지역 수", len(df))
        st.metric("평균 불편 지수", f"{df[EVSchema.discomfort_index].mean():.2f}")
        
        st.markdown("---")
        st.subheader("🔍 필터링")
        
        # 지역 선택
        selected_region = st.selectbox(
            "지역 선택",
            options=['전체'] + df[EVSchema.region].tolist(),
            index=0
        )
        
        # 순위 범위 필터
        min_rank = int(df[EVSchema.discomfort_rank].min())
        max_rank = int(df[EVSchema.discomfort_rank].max())
        rank_range = st.slider(
            "불편 순위 범위",
            min_value=min_rank,
            max_value=max_rank,
            value=(min_rank, max_rank)
        )
        
        st.markdown("---")
        st.info("💡 **데이터 설명**\n"
                "- **불편 지수**: 수요(전기차 수)에서 공급(충전기 수)을 뺀 값\n"
                "- 지수가 높을수록 충전 인프라가 부족함을 의미")
                
    return selected_region, rank_range
