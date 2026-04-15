import pandas as pd

def load_ev_data():
    """
    전국 시도별 전기차 등록 현황 및 충전 인프라 데이터를 로드하고 전처리합니다.
    
    Returns:
        pd.DataFrame: 다음과 같은 컬럼을 포함하는 데이터프레임
            - 시도, 전기차_등록수, 충전소_수, 충전기_대수, 인구수, 면적_km2, 위도, 경도
            - 수요_밀도: 인구 만 명당 전기차 수
            - 공급_밀도: 면적 100km^2당 충전기 수
            - 불편_지수: 수요 밀도 - 공급 밀도 (지수가 높을수록 인프라 부족)
            - 불편_순위: 불편 지수에 따른 전국 순위
    """
    # 1) 시도별 전기차 등록 현황 (가상 데이터)
    data = {
        '시도': ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'],
        '전기차_등록수': [450000, 120000, 80000, 95000, 50000, 45000, 40000, 35000, 520000, 70000, 60000, 85000, 55000, 75000, 90000, 110000, 65000],
        '충전소_수': [12000, 3500, 2200, 2800, 1500, 1300, 1100, 1000, 15000, 2000, 1800, 2500, 1600, 2200, 2700, 3200, 1900],
        '충전기_대수': [35000, 9000, 6000, 7500, 4000, 3500, 3000, 2800, 42000, 5500, 5000, 7000, 4500, 6000, 7500, 8500, 5500],
        # 필수아님
        '인구수': [9700000, 3400000, 2400000, 2900000, 1400000, 1450000, 1150000, 370000, 13500000, 1550000, 1580000, 2180000, 1780000, 1840000, 2640000, 3350000, 670000],
        # 필수아님
        '면적_km2': [605, 770, 840, 1063, 501, 541, 1063, 614, 10184, 18384, 11858, 10594, 11812, 18392, 10515, 10533, 1849],
        '위도': [37.5665, 35.1796, 35.8714, 37.4563, 35.1597, 36.3504, 35.5384, 36.4800, 37.5665, 38.0336, 36.6355, 36.6589, 35.8242, 34.8163, 36.5746, 35.2033, 33.4996],
        '경도': [126.9780, 129.0757, 128.6014, 126.7052, 126.8507, 127.3845, 129.3115, 127.2499, 127.0000, 128.1667, 127.4984, 126.7052, 127.1530, 126.3663, 128.7471, 128.4161, 126.5312]
    }
    df = pd.DataFrame(data)
    
    # 2) 충전 불편 지수 계산 (수요 대비 공급)
    df['수요_밀도'] = (df['전기차_등록수'] / df['인구수']) * 10000
    df['공급_밀도'] = (df['충전기_대수'] / df['면적_km2']) * 100
    # (불편 지수는 단순 전기차_등록수와 충전기_대수를 비교해도 됨)
    df['불편_지수'] = df['수요_밀도'] - df['공급_밀도']
    
    # 3) 순위 계산
    df['불편_순위'] = df['불편_지수'].rank(ascending=False).astype(int)
    
    return df

def filter_data(df, selected_region, rank_range):
    """
    사용자가 선택한 지역 및 불편 순위 범위에 따라 데이터를 필터링합니다.

    Args:
        df (pd.DataFrame): 원본 데이터프레임
        selected_region (str): 선택된 지역 (예: '전체', '서울')
        rank_range (tuple): 선택된 불편 순위 범위 (min, max)

    Returns:
        pd.DataFrame: 필터링된 결과 데이터프레임
    """
    if selected_region != '전체':
        df_filtered = df[df['시도'] == selected_region]
    else:
        df_filtered = df.copy()

    # 순위 범위 필터 적용
    df_filtered = df_filtered[(df_filtered['불편_순위'] >= rank_range[0]) & 
                            (df_filtered['불편_순위'] <= rank_range[1])]
    
    return df_filtered

def load_ev_data_csv():
    """
    CSV 파일들로부터 데이터를 로드하여 연도별/지역별 중첩 딕셔너리 형태로 반환합니다.
    
    Returns:
        dict: {년도: {시도: {지역, 전기차 등록수, 충전기 대수, 충전소 수}}}
    """
    from pathlib import Path

    # 1. 경로 설정
    base_path = Path(__file__).parent / "src_clean" / "한국전력공사_지역별 현황정보"
    
    file_ev = base_path / "전기차_18-24_year.csv"
    file_charger = base_path / "충전기_16-24_year.csv"
    file_station = base_path / "충전소_16-24_year.csv"

    # 2. 지역명 정규화 매퍼
    REGION_MAP = {
        '서울특별시': '서울', '인천광역시': '인천', '대전광역시': '대전', '대구광역시': '대구',
        '광주광역시': '광주', '울산광역시': '울산', '부산광역시': '부산', '세종특별자치시': '세종',
        '경기도': '경기', '강원도': '강원', '충청북도': '충북', '충청남도': '충남',
        '전라북도': '전북', '전라남도': '전남', '경상북도': '경북', '경상남도': '경남',
        '제주특별자치도': '제주'
    }

    def process_csv(path, value_name):
        df = pd.read_csv(path)
        # '합계' 행 제외
        df = df[df['지역'] != '합계']
        # 지역명 정규화
        df['지역'] = df['지역'].replace(REGION_MAP)
        # Wide to Long (연도 컬럼을 행으로 변환)
        df_melted = df.melt(id_vars=['지역'], var_name='연도', value_name=value_name)
        return df_melted

    # 3. 데이터 로드 및 전처리
    df_ev = process_csv(file_ev, '전기차 등록수')
    df_charger = process_csv(file_charger, '충전기 대수')
    df_station = process_csv(file_station, '충전소 수')

    # 4. 데이터 병합 (Outer join으로 누락된 연도 대응)
    merged_df = pd.merge(df_ev, df_charger, on=['지역', '연도'], how='outer')
    merged_df = pd.merge(merged_df, df_station, on=['지역', '연도'], how='outer')

    # 5. 수치형 데이터 정수 변환 및 결측치 처리
    cols = ['전기차 등록수', '충전기 대수', '충전소 수']
    merged_df[cols] = merged_df[cols].fillna(0).astype(int)

    # 6. 중첩 딕셔너리 변환 (2018년도 이후 데이터만 포함)
    result = {}
    for _, row in merged_df.iterrows():
        year = str(row['연도'])
        region = row['지역']
        
        # 2016, 2017년 제외
        if int(year) < 2018:
            continue
            
        if year not in result:
            result[year] = {}
        
        result[year][region] = {
            '지역': region,
            '전기차 등록수': row['전기차 등록수'],
            '충전기 대수': row['충전기 대수'],
            '충전소 수': row['충전소 수']
        }
    
    return result
