"""
ev_charger_all_clean.csv 를 MySQL DB에 업로드하는 스크립트

실행 방법:
    프로젝트 루트에서: python -m domain.ev_charger_csv_to_db
"""

import pandas as pd
from pathlib import Path
from config.db_manager import db

# CSV 파일 경로 (프로젝트 루트 기준)
CSV_PATH = Path(__file__).resolve().parent.parent / "ev_charger_all_clean.csv"

# 업로드할 테이블 이름
TABLE_NAME = "ev_charger"

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    statNm      VARCHAR(100),
    statId      VARCHAR(50),
    chgerId     VARCHAR(10),
    chgerType   VARCHAR(10),
    addr        VARCHAR(200),
    addrDetail  VARCHAR(200),
    location    VARCHAR(200),
    useTime     VARCHAR(100),
    lat         DOUBLE,
    lng         DOUBLE,
    busiId      VARCHAR(20),
    bnm         VARCHAR(100),
    busiNm      VARCHAR(100),
    busiCall    VARCHAR(50),
    stat        VARCHAR(10),
    statUpdDt   VARCHAR(20),
    lastTsdt    VARCHAR(20),
    lastTedt    VARCHAR(20),
    nowTsdt     VARCHAR(20),
    powerType   VARCHAR(20),
    output      INT,
    method      VARCHAR(20),
    zcode       VARCHAR(10),
    zscode      VARCHAR(10),
    kind        VARCHAR(10),
    kindDetail  VARCHAR(10),
    parkingFree VARCHAR(5),
    note        TEXT,
    limitYn     VARCHAR(5),
    limitDetail VARCHAR(200),
    delYn       VARCHAR(5),
    delDetail   VARCHAR(200),
    trafficYn   VARCHAR(5),
    year        VARCHAR(10),
    floorNum    VARCHAR(10),
    floorType   VARCHAR(5),
    maker       VARCHAR(50)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

INSERT_SQL = f"""
INSERT INTO `{TABLE_NAME}` (
    statNm, statId, chgerId, chgerType, addr, addrDetail, location, useTime,
    lat, lng, busiId, bnm, busiNm, busiCall, stat, statUpdDt, lastTsdt, lastTedt,
    nowTsdt, powerType, output, method, zcode, zscode, kind, kindDetail,
    parkingFree, note, limitYn, limitDetail, delYn, delDetail, trafficYn,
    year, floorNum, floorType, maker
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s
)
"""


def load_csv() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", dtype=str)
    # NaN → None (MySQL NULL 처리)
    df = df.where(pd.notna(df), None)
    return df


def create_table():
    success = db.execute_query(CREATE_TABLE_SQL)
    if success:
        print(f"테이블 '{TABLE_NAME}' 준비 완료")
    else:
        raise RuntimeError("테이블 생성 실패")


def insert_rows(df: pd.DataFrame):
    columns = [
        "statNm", "statId", "chgerId", "chgerType", "addr", "addrDetail", "location", "useTime",
        "lat", "lng", "busiId", "bnm", "busiNm", "busiCall", "stat", "statUpdDt", "lastTsdt", "lastTedt",
        "nowTsdt", "powerType", "output", "method", "zcode", "zscode", "kind", "kindDetail",
        "parkingFree", "note", "limitYn", "limitDetail", "delYn", "delDetail", "trafficYn",
        "year", "floorNum", "floorType", "maker",
    ]

    conn = db.connect()
    if not conn:
        raise RuntimeError("DB 연결 실패")

    cursor = conn.cursor()
    try:
        rows = [tuple(row[col] for col in columns) for _, row in df.iterrows()]
        cursor.executemany(INSERT_SQL, rows)
        conn.commit()
        print(f"{cursor.rowcount}건 삽입 완료")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def main():
    print(f"CSV 로드 중: {CSV_PATH}")
    df = load_csv()
    print(f"총 {len(df)}건 로드됨")

    create_table()
    insert_rows(df)
    print("업로드 완료!")


if __name__ == "__main__":
    main()
