import pandas as pd
import os

# 1. 경로 설정 (프로젝트 루트 폴더 기준)
base_path = 'domain/data'
target_path = 'domain/result'
file_name = '201001_202510_지역별_전기차_등록_현황(누적).csv'

# 전체 경로 결합
file_path = os.path.join(base_path, file_name)
output_path = os.path.join(target_path, f"transposed_{file_name}")

# 결과 폴더가 없으면 생성
if not os.path.exists(target_path):
    os.makedirs(target_path)

# 2. 데이터 처리 및 파일 생성
try:
    # 상단 메타데이터 3줄 제외 후 읽기
    df = pd.read_csv(file_path, skiprows=3, encoding='utf-8-sig')
    
    # 행과 열 바꾸기 (Transpose)
    df_transposed = df.transpose().reset_index()
    
    # CSV 파일로 저장 (인덱스 및 헤더 제외하여 구조 유지)
    df_transposed.to_csv(output_path, index=False, header=False, encoding='utf-8-sig')
    
    print(f"파일 생성 완료: {output_path}")

except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_path}")
except Exception as e:
    print(f"오류 발생: {e}")