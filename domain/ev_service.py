import pandas as pd
import pandera as pa
from pandera.typing import Series
import warnings

def load_ev_data():
    """
    전국 시도별 전기차 등록 현황 및 충전 인프라 데이터를 로드하고 전처리합니다.
    """
    # 1) 시도별 전기차 등록 현황 (가상 데이터)
    data = {
        EVSchema.region: ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'],
        EVSchema.ev_count: [450000, 120000, 80000, 95000, 50000, 45000, 40000, 35000, 520000, 70000, 60000, 85000, 55000, 75000, 90000, 110000, 65000],
        EVSchema.station_count: [12000, 3500, 2200, 2800, 1500, 1300, 1100, 1000, 15000, 2000, 1800, 2500, 1600, 2200, 2700, 3200, 1900],
        EVSchema.charger_count: [35000, 9000, 6000, 7500, 4000, 3500, 3000, 2800, 42000, 5500, 5000, 7000, 4500, 6000, 7500, 8500, 5500],
        EVSchema.population: [9700000, 3400000, 2400000, 2900000, 1400000, 1450000, 1150000, 370000, 13500000, 1550000, 1580000, 2180000, 1780000, 1840000, 2640000, 3350000, 670000],
        EVSchema.area: [605, 770, 840, 1063, 501, 541, 1063, 614, 10184, 18384, 11858, 10594, 11812, 18392, 10515, 10533, 1849],
        EVSchema.lat: [37.5665, 35.1796, 35.8714, 37.4563, 35.1597, 36.3504, 35.5384, 36.4800, 37.5665, 38.0336, 36.6355, 36.6589, 35.8242, 34.8163, 36.5746, 35.2033, 33.4996],
        EVSchema.lon: [126.9780, 129.0757, 128.6014, 126.7052, 126.8507, 127.3845, 129.3115, 127.2499, 127.0000, 128.1667, 127.4984, 126.7052, 127.1530, 126.3663, 128.7471, 128.4161, 126.5312]
    }
    df = pd.DataFrame(data)
    
    # 2) 충전 불편 지수 계산
    df[EVSchema.demand_density] = (df[EVSchema.ev_count] / df[EVSchema.population]) * 10000
    df[EVSchema.supply_density] = (df[EVSchema.charger_count] / df[EVSchema.area]) * 100
    df[EVSchema.discomfort_index] = df[EVSchema.demand_density] - df[EVSchema.supply_density]
    
    # 3) 순위 계산
    df[EVSchema.discomfort_rank] = df[EVSchema.discomfort_index].rank(ascending=False).astype(int)
    
    return validate_ev_data(df)

def filter_data(df, selected_region, rank_range):
    """
    사용자가 선택한 지역 및 불편 순위 범위에 따라 데이터를 필터링합니다.
    """
    if selected_region != '전체':
        df_filtered = df[df[EVSchema.region] == selected_region]
    else:
        df_filtered = df.copy()

    # 순위 범위 필터 적용
    df_filtered = df_filtered[(df_filtered[EVSchema.discomfort_rank] >= rank_range[0]) & 
                            (df_filtered[EVSchema.discomfort_rank] <= rank_range[1])]
    
    return df_filtered

def load_ev_data_csv():
    """
    CSV 파일들로부터 데이터를 로드하여 연도별/지역별 중첩 딕셔너리 형태로 반환합니다.
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
        df_melted = df.melt(id_vars=['지역'], var_name=EVSchema.year, value_name=value_name)
        return df_melted

    # 3. 데이터 로드 및 전처리 (컬럼명 표준화)
    df_ev = process_csv(file_ev, EVSchema.ev_count)
    df_charger = process_csv(file_charger, EVSchema.charger_count)
    df_station = process_csv(file_station, EVSchema.station_count)

    # 4. 데이터 병합 (Outer join으로 누락된 연도 대응)
    merged_df = pd.merge(df_ev, df_charger, on=['지역', EVSchema.year], how='outer')
    merged_df = pd.merge(merged_df, df_station, on=['지역', EVSchema.year], how='outer')
    
    # 5. 컬럼명 표준화 ('지역' -> EVSchema.region)
    merged_df = merged_df.rename(columns={'지역': EVSchema.region})

    # 6. 수치형 데이터 정수 변환 및 결측치 처리
    cols = [EVSchema.ev_count, EVSchema.charger_count, EVSchema.station_count]
    merged_df[cols] = merged_df[cols].fillna(0).astype(int)

    # 7. 중첩 딕셔너리 변환 (2018년도 이후 데이터만 포함)
    result = {}
    for _, row in merged_df.iterrows():
        year = str(row[EVSchema.year])
        region = row[EVSchema.region]
        
        # 2016, 2017년 제외
        if int(year) < 2018:
            continue
            
        if year not in result:
            result[year] = {}
        
        result[year][region] = {
            EVSchema.region: region,
            EVSchema.ev_count: row[EVSchema.ev_count],
            EVSchema.charger_count: row[EVSchema.charger_count],
            EVSchema.station_count: row[EVSchema.station_count]
        }
    
    return result

# =================================================================
# Pandera Schema & Validation Helpers
# =================================================================

class EVSchema(pa.DataFrameModel):
    """
    전기차 데이터 규격 정의 (Pandera)
    속성명은 영어(코드용), 값은 한국어(데이터 매핑용)로 구성합니다.
    """
    region: Series[str] = pa.Field(alias="시도")
    ev_count: Series[int] = pa.Field(alias="전기차_등록수", ge=0)
    station_count: Series[int] = pa.Field(alias="충전소_수", ge=0)
    charger_count: Series[int] = pa.Field(alias="충전기_대수", ge=0)
    
    # 필수 아님 (Optional 필드는 nullable=True 혹은 스키마에서 제외 가능)
    population: Series[int] = pa.Field(alias="인구수", ge=0, nullable=True)
    area: Series[float] = pa.Field(alias="면적_km2", ge=0, nullable=True)
    lat: Series[float] = pa.Field(alias="위도", nullable=True)
    lon: Series[float] = pa.Field(alias="경도", nullable=True)
    
    # 분석 결과 필드
    demand_density: Series[float] = pa.Field(alias="수요_밀도", nullable=True)
    supply_density: Series[float] = pa.Field(alias="공급_밀도", nullable=True)
    discomfort_index: Series[float] = pa.Field(alias="불편_지수", nullable=True)
    discomfort_rank: Series[int] = pa.Field(alias="불편_순위", ge=1, nullable=True)
    
    # 연도 (CSV용)
    year: Series[str] = pa.Field(alias="연도")

    class Config:
        strict = False # 정의되지 않은 컬럼이 있어도 허용
        coerce = True  # 타입 자동 변환 허용

def validate_ev_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pandera를 사용하여 DataFrame 규격을 검증합니다.
    실패 시 에러를 발생시키지 않고 Warning만 출력합니다.
    """
    try:
        return EVSchema.validate(df)
    except pa.errors.SchemaError as e:
        warnings.warn(f"데이터 규격 검증 실패 (일부 데이터가 누락되거나 형식이 다를 수 있습니다): {e}")
        return df