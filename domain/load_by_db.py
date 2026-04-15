from config import db
import pandas as pd
import domain.load_by_csv as csv

# 전기차/충전기 파일의 지역명 형식이 달라 통일하기 위한 매퍼
REGION_MAP = {
    '서울특별시': '서울', '인천광역시': '인천', '대전광역시': '대전', '대구광역시': '대구',
    '광주광역시': '광주', '울산광역시': '울산', '부산광역시': '부산', '세종특별자치시': '세종',
    '경기도': '경기', '강원도': '강원', '충청북도': '충북', '충청남도': '충남',
    '전라북도': '전북', '전라남도': '전남', '경상북도': '경북', '경상남도': '경남',
    '제주특별자치도': '제주',
    # 충전기 파일에서 사용하는 변형 이름 추가
    '강원특별자치도': '강원', '전북특별자치도': '전북',
}

def create_ev_infrastructure_stats():
    db.execute_query("DROP TABLE IF EXISTS ev_infrastructure_stats")
    create_sql = """
    CREATE TABLE ev_infrastructure_stats (
        year INT NOT NULL,
        location VARCHAR(50) NOT NULL,
        total_ev_registration INT NOT NULL,
        total_ev_charger INT NOT NULL,
        PRIMARY KEY (year, location)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    db.execute_query(create_sql)

def batch_insert_ev_infrastructure_stats():
    """
    CSV 파일에서 연도별/지역별 전기차 등록수 및 충전기 수를 읽어
    ev_infrastructure_stats 테이블에 배치 INSERT합니다.
    (2018년 ~ 2024년 데이터만 삽입)
    """

    df_ev = csv.process_csv(csv.EV_CSV_PATH.ev_car, 'total_ev_registration')
    df_charger = csv.process_csv(csv.EV_CSV_PATH.ev_charger, 'total_ev_charger')

    merged = pd.merge(df_ev, df_charger, on=['지역', 'year'], how='outer')
    merged = merged[merged['year'] >= 2018].copy()
    merged[['total_ev_registration', 'total_ev_charger']] = (
        merged[['total_ev_registration', 'total_ev_charger']].fillna(0).astype(int)
    )

    rows = [
        (int(row['year']), row['지역'], int(row['total_ev_registration']), int(row['total_ev_charger']))
        for _, row in merged.iterrows()
    ]

    print(f"총 {len(rows)}건을 INSERT합니다...")

    inserted = db.execute_many("""
        INSERT INTO ev_infrastructure_stats
            (year, location, total_ev_registration, total_ev_charger)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            total_ev_registration = VALUES(total_ev_registration),
            total_ev_charger      = VALUES(total_ev_charger)
    """, rows)

    if inserted >= 0:
        print(f"✅ 배치 INSERT 완료: {inserted}건 처리됨")
    else:
        print("❌ INSERT 실패 (DB 로그 확인 필요)")

    return inserted

def load_ev() -> list[dict]:
    return db.fetch_all("""
    select * from ev_infrastructure_stats 
    """)

def load_ev_by_year(ev) -> dict:
    """
    DB에서 전체 데이터를 로드하여 연도별/지역별로 그룹핑합니다.

    Returns:
        dict: {년도(str): {지역(str): {year, location, total_ev_registration, total_ev_charger}}}
    """

    result: dict = {}
    for row in ev:
        year = str(row['year'])
        region = row['location']
        if year not in result:
            result[year] = {}
        result[year][region] = row

    return result

def load_ev_by_region(ev) -> dict:
    """
    DB에서 전체 데이터를 로드하여 지역별/연도별로 그룹핑합니다.

    Returns:
        dict: {지역(str): {년도(str): {year, location, total_ev_registration, total_ev_charger}}}
    """

    result: dict = {}
    for row in ev:
        year = str(row['year'])
        region = row['location']
        if region not in result:
            result[region] = {}
        result[region][year] = row

    return result
