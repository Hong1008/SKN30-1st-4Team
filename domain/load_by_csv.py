from enum import Enum
from pathlib import Path

import pandas as pd
from domain.ev_schema import EVSchema


class EV_CSV_PATH(Enum):
    ev_car = "전기차_등록_현황_광역_통합.csv"
    ev_charger = "전기차_충전기_합계_연도별_변환.csv"


def process_csv(path: EV_CSV_PATH, value_name):
    base_path = Path(__file__).parent / "src_clean"
    file = base_path / path.value
    df = pd.read_csv(file)
    # '합계' 행 제외
    df = df[df["지역"] != "합계"]
    # Wide to Long (연도 컬럼을 행으로 변환)
    df_melted = df.melt(id_vars=["지역"], var_name=EVSchema.year, value_name=value_name)
    return df_melted

def load_ev():
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
    df_ev = process_csv(EV_CSV_PATH.ev_car, EVSchema.ev_count)
    df_charger = process_csv(EV_CSV_PATH.ev_charger, EVSchema.charger_count)

    merged_df = pd.merge(df_ev, df_charger, on=["지역", EVSchema.year], how="outer")
    merged_df = merged_df.rename(columns={"지역": EVSchema.region})

    cols = [EVSchema.ev_count, EVSchema.charger_count]
    merged_df[cols] = merged_df[cols].fillna(0).astype(int)

    # 2020년도 이후 데이터만 필터링
    merged_df = merged_df[merged_df[EVSchema.year].astype(int) >= 2020]

    # 지역별 메타데이터(인구, 면적, 위경도) 매핑
    for field in [EVSchema.population, EVSchema.area, EVSchema.lat, EVSchema.lon]:
        merged_df[field] = merged_df[EVSchema.region].map(lambda r: meta_lookup.get(r, {}).get(field))

    # 불편 지수(TCII) 계산
    # 수식: w1 * (EV / Charger) + w2 * sqrt(Area / Charger) 
    chargers = merged_df[EVSchema.charger_count].replace(0, 1)  # 분모 0 방지
    
    # 가중치 (초기값으로 모두 1 부여, 필요에 따라 수정 가능)
    w1, w2 = 2.0, 1.0
    
    # 1. 기기 경쟁 (EV / Charger)
    comp_term = merged_df[EVSchema.ev_count] / chargers
    # 2. 공간적 거리 (sqrt(Area / Charger))
    dist_term = (merged_df[EVSchema.area] / chargers) ** 0.5
    
    merged_df[EVSchema.discomfort_index] = (w1 * comp_term + w2 * dist_term ).round(2)

    return merged_df.reset_index(drop=True)

def load_ev_by_year():
    """
    CSV 파일들로부터 데이터를 로드하여 연도별/지역별 중첩 딕셔너리 형태로 반환합니다.
    """
    df_ev = process_csv(EV_CSV_PATH.ev_car, EVSchema.ev_count)
    df_charger = process_csv(EV_CSV_PATH.ev_charger, EVSchema.charger_count)

    merged_df = pd.merge(df_ev, df_charger, on=["지역", EVSchema.year], how="outer")
    merged_df = merged_df.rename(columns={"지역": EVSchema.region})

    cols = [EVSchema.ev_count, EVSchema.charger_count]
    merged_df[cols] = merged_df[cols].fillna(0).astype(int)

    result = {}
    for _, row in merged_df.iterrows():
        year = str(row[EVSchema.year])
        region = row[EVSchema.region]

        # 2016, 2017년 제외
        if int(year) < 2018:
            continue

        if year not in result:
            result[year] = {}

        # 충전기 1대당 전기차 수 (값이 클수록 충전이 불편함을 의미)
        charger = row[EVSchema.charger_count] if row[EVSchema.charger_count] > 0 else 1
        result[year][region] = {
            EVSchema.year: year,
            EVSchema.region: region,
            EVSchema.ev_count: row[EVSchema.ev_count],
            EVSchema.charger_count: row[EVSchema.charger_count],
            EVSchema.discomfort_index: round(row[EVSchema.ev_count] / charger, 2),
        }

    # 순위 계산: 연도별로 discomfort_index 기준 내림차순 순위
    for year, regions in result.items():
        indices = {r: d[EVSchema.discomfort_index] for r, d in regions.items()}
        sorted_regions = sorted(indices, key=indices.get, reverse=True)
        for rank, r in enumerate(sorted_regions, start=1):
            regions[r][EVSchema.discomfort_rank] = rank

    return result


def load_ev_by_region() -> dict:
    """
    load_ev_by_year()의 결과를 EVSchema.region(지역) 기준으로 재구성합니다.

    Returns:
        dict: {지역: {년도: {ev_count, charger_count, station_count}}}
    """
    year_first = load_ev_by_year()  # {년도: {지역: {...}}}

    result: dict = {}
    for year, regions in year_first.items():
        for region, data in regions.items():
            if region not in result:
                result[region] = {}
            result[region][year] = data

    return result
