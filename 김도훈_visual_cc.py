import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 설정
st.set_page_config(page_title="EV Status Dashboard", layout="wide")
st.title("⚡ 전국 지역별 전기차 보급 현황 대시보드")

@st.cache_data
def load_and_clean_data():
    # 실행 파일 위치 기준 경로 설정
    base_path = os.path.dirname(os.path.abspath(__file__))
    target_file = '한국전력공사_지역별 전기차 현황정보_combined_version.csv'
    
    # 1순위: domain/source 폴더, 2순위: 현재 폴더 탐색
    file_path = os.path.join(base_path, 'domain', 'source', target_file)
    if not os.path.exists(file_path):
        file_path = os.path.join(base_path, target_file)

    if not os.path.exists(file_path):
        st.error(f"⚠️ 파일을 찾을 수 없습니다. 경로를 확인하세요.")
        st.info(f"확인된 경로: {file_path}")
        return None, None

    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df['기준일'] = pd.to_datetime(df['기준일'])
        df = df.sort_values('기준일')
        
        regions = ['부산', '대구', '대전', '광주', '경기', '강원', '경북', '경남', 
                   '충북', '충남', '전북', '전남', '세종', '서울', '인천', '울산', '제주']
        
        # 데이터 정제: 결측치 0 처리 및 정수 변환
        df[regions] = df[regions].fillna(0).astype(int)
        df['합계'] = df[regions].sum(axis=1)
        
        return df, regions
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
        return None, None

df, regions = load_and_clean_data()

# 데이터 로드 성공 시 시각화
if df is not None:
    latest_data = df.iloc[-1]
    st.success(f"✅ 데이터 로드 성공! ({latest_data['기준일'].strftime('%Y-%m-%d')} 기준)")
    
    # [추가 기능] 지역 선택 필터
    st.sidebar.header("🔍 상세 필터")
    selected_regions = st.sidebar.multiselect("비교할 지역을 선택하세요", regions, default=['서울', '경기', '제주'])

    # 섹션 1: 차트 시각화
    col1, col2 = st.columns(2)
    with col1:
        # 전체 합계 혹은 선택 지역 추이 시각화
        fig_line = px.line(df, x='기준일', y=selected_regions if selected_regions else '합계', 
                           markers=True, title="지역별 전기차 누적 성장 추이")
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col2:
        pie_df = pd.DataFrame({'지역': regions, '대수': latest_data[regions].values})
        fig_pie = px.pie(pie_df, values='대수', names='지역', hole=0.4, title="전국 지역별 보급 비중")
        st.plotly_chart(fig_pie, use_container_width=True)

    # 섹션 2: 데이터 표 시각화
    st.divider()
    st.subheader("📋 지역별 전기차 등록 현황 상세 테이블")
    
    formatted_df = df.copy()
    formatted_df['기준일'] = formatted_df['기준일'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        formatted_df.style.format({col: "{:,}" for col in regions + ['합계']}),
        use_container_width=True
    )

    # 섹션 3: 데이터 다운로드 (CSV & XML) - 최적화 완료
    st.divider()
    st.subheader("📥 정제된 데이터 내보내기")
    
    dl_col1, dl_col2 = st.columns(2)
    
    with dl_col1:
        # CSV 다운로드
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📄 CSV 파일로 저장",
            data=csv_data,
            file_name='ev_status_data.csv',
            mime='text/csv',
            use_container_width=True
        )
        
    with dl_col2:
        # XML 다운로드: 불필요한 예외 구문 제거
        xml_data = df.to_xml(index=False, encoding='utf-8')
        st.download_button(
            label="📁 XML 파일로 저장",
            data=xml_data,
            file_name='ev_status_data.xml',
            mime='application/xml',
            use_container_width=True
        )