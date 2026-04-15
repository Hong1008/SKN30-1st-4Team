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

        result[year][region] = {
            EVSchema.year: year,
            EVSchema.region: region,
            EVSchema.ev_count: row[EVSchema.ev_count],
            EVSchema.charger_count: row[EVSchema.charger_count],
        }

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
