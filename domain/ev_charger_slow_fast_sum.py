import pandas as pd
import os

# 1. 파일이 들어있는 정확한 폴더 경로
base_path = 'domain/src_raw'
file_name = '201001_202510_지역별_전기차_충전기_구축현황(누적).csv'

# 전체 경로 결합
file_path = os.path.join(base_path, file_name)

# 2. 파일 읽기 (상단 타이틀 3줄 제외)
try:
    df = pd.read_csv(file_path, skiprows=3)
    print(f"✅ 파일을 성공적으로 읽었습니다: {file_path}")
except FileNotFoundError:
    print(f"❌ 파일을 찾을 수 없습니다. 경로를 확인하세요: {file_path}")
    exit()

# 3. 숫자 데이터 컬럼 설정 및 변환
region_cols = ['서울', '경기', '인천', '강원', '충청', '전라', '경상', '제주', '합계']
for col in region_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# 4. '년월' 기준 합산 (완속+급속 통합)
df_total = df.groupby('년월')[region_cols].sum().reset_index()

# 5. 결과 파일 저장 (같은 폴더에 저장)
output_file = os.path.join(base_path, '전기차_충전기_합계_현황.csv')
df_total.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✅ 합계 파일 생성 완료: {output_file}")