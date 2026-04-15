import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series


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