import warnings

from domain.load_by_csv import load_ev_by_year, load_ev_by_region
from domain.ev_schema import EVSchema
import pandas as pd
import pandera.pandas as pa


def load_ev_data():
    """
    전국 시도별 전기차 등록 현황 및 충전 인프라 데이터를 로드하고 전처리합니다.
    """
    # 1) 시도별 전기차 등록 현황 (가상 데이터)
    data = {
        EVSchema.region: [
            '강원도',
            '경기도',
            '경상도',
            '서울특별시',
            '인천광역시',
            '전라도',
            '제주특별자치도',
            '충청도',
        ],
        EVSchema.population: [9700000, 3400000, 2400000, 2900000, 1400000, 1450000, 1150000, 370000, 13500000, 1550000, 1580000, 2180000, 1780000, 1840000, 2640000, 3350000, 670000],
        EVSchema.area: [605, 770, 840, 1063, 501, 541, 1063, 614, 10184, 18384, 11858, 10594, 11812, 18392, 10515, 10533, 1849],
        EVSchema.lat: [37.5665, 35.1796, 35.8714, 37.4563, 35.1597, 36.3504, 35.5384, 36.4800, 37.5665, 38.0336, 36.6355, 36.6589, 35.8242, 34.8163, 36.5746, 35.2033, 33.4996],
        EVSchema.lon: [126.9780, 129.0757, 128.6014, 126.7052, 126.8507, 127.3845, 129.3115, 127.2499, 127.0000, 128.1667, 127.4984, 126.7052, 127.1530, 126.3663, 128.7471, 128.4161, 126.5312]
    }

    # 메타데이터 lookup 생성 {지역명: {population, area, lat, lon}}
    meta_lookup = {}
    for i, r in enumerate(data[EVSchema.region]):
        meta_lookup[r] = {
            EVSchema.population: data[EVSchema.population][i],
            EVSchema.area: data[EVSchema.area][i],
            EVSchema.lat: data[EVSchema.lat][i],
            EVSchema.lon: data[EVSchema.lon][i],
        }

    # if settings.USE_DB:
    #     ev = db.load_ev()
    #     year = db.load_ev_by_year(ev)
    #     region = db.load_ev_by_region(ev)
    # else:
    year = load_ev_by_year()
    region = load_ev_by_region()

    # 2) year 딕셔너리에 메타데이터 삽입
    for y, regions in year.items():
        for r, info in regions.items():
            if r in meta_lookup:
                info.update(meta_lookup[r])

    # 3) region 딕셔너리에 메타데이터 삽입
    for r, years in region.items():
        if r in meta_lookup:
            for y, info in years.items():
                info.update(meta_lookup[r])

    df_year = pd.DataFrame(year)
    df_region = pd.DataFrame(region)

    return df_year, df_region

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


# =================================================================
# Pandera Schema & Validation Helpers
# =================================================================



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