import warnings

from domain.load_by_csv import load_ev_by_year, load_ev_by_region
from domain.ev_schema import EVSchema
import pandas as pd
import pandera.pandas as pa



def load_ev_data_old():
    """
    전국 시도별 전기차 등록 현황 및 충전 인프라 데이터를 로드하고 전처리합니다.
    """
    # 1) 시도별 전기차 등록 현황 (가상 데이터)
    data = {
        EVSchema.region: [
            '서울특별시',
            '경상도',
            '강원도',
            '경기도',
            '인천광역시',
            '전라도',
            '제주특별자치도',
            '충청도',
        ],
        EVSchema.population: [9400000, 13000000, 1500000, 13600000, 3000000, 5000000, 670000, 5500000],
        EVSchema.area: [605, 32000, 16875, 10171, 1062, 20900, 1849, 16600],
        EVSchema.lat: [37.5665, 35.8000, 37.8228, 37.2636, 37.4563, 35.8000, 33.4996, 36.6000],
        EVSchema.lon: [126.9780, 128.5000, 128.1555, 127.0286, 126.7052, 127.1000, 126.5312, 127.5000]
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