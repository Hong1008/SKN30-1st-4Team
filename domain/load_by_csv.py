from enum import Enum
from pathlib import Path

import pandas as pd
from domain.ev_schema import EVSchema


class EV_CSV_PATH(Enum):
    ev_car = "전기차_18-24_year.csv"
    ev_charger = "충전기_16-24_year.csv"
    ev_station = "충전소_16-24_year.csv"


def process_csv(path: EV_CSV_PATH, value_name):
    base_path = Path(__file__).parent / "src_clean" / "한국전력공사_지역별 현황정보"
    file = base_path / path.value
    REGION_MAP = {
        "서울특별시": "서울",
        "인천광역시": "인천",
        "대전광역시": "대전",
        "대구광역시": "대구",
        "광주광역시": "광주",
        "울산광역시": "울산",
        "부산광역시": "부산",
        "세종특별자치시": "세종",
        "경기도": "경기",
        "강원도": "강원",
        "충청북도": "충북",
        "충청남도": "충남",
        "전라북도": "전북",
        "전라남도": "전남",
        "경상북도": "경북",
        "경상남도": "경남",
        "제주특별자치도": "제주",
    }
    df = pd.read_csv(file)
    # '합계' 행 제외
    df = df[df["지역"] != "합계"]
    # 지역명 정규화
    df["지역"] = df["지역"].replace(REGION_MAP)
    # Wide to Long (연도 컬럼을 행으로 변환)
    df_melted = df.melt(id_vars=["지역"], var_name=EVSchema.year, value_name=value_name)
    return df_melted


def load_ev_by_year():
    """
    CSV 파일들로부터 데이터를 로드하여 연도별/지역별 중첩 딕셔너리 형태로 반환합니다.
    """
    df_ev = process_csv(EV_CSV_PATH.ev_car, EVSchema.ev_count)
    df_charger = process_csv(EV_CSV_PATH.ev_charger, EVSchema.charger_count)
    df_station = process_csv(EV_CSV_PATH.ev_station, EVSchema.station_count)

    merged_df = pd.merge(df_ev, df_charger, on=["지역", EVSchema.year], how="outer")
    merged_df = pd.merge(merged_df, df_station, on=["지역", EVSchema.year], how="outer")
    merged_df = merged_df.rename(columns={"지역": EVSchema.region})

    cols = [EVSchema.ev_count, EVSchema.charger_count, EVSchema.station_count]
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
            EVSchema.station_count: row[EVSchema.station_count],
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
