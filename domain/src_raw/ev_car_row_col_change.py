import pandas as pd
import os

# 1. 절대 경로 설정 (스크립트 파일 위치 기준)
# 현재 파일: domain/src_raw/ev_car_row_col_change.py
current_dir = os.path.dirname(os.path.abspath(__file__)) # src_raw 폴더
parent_dir = os.path.dirname(current_dir)                # domain 폴더

# 경로 정의
source_dir = os.path.join(parent_dir, 'data')
target_dir = os.path.join(parent_dir, 'result')

print(f"--- 경로 점검 ---")
print(f"데이터 폴더 위치: {source_dir}")
print(f"결과 저장 위치: {target_dir}")

# 2. 데이터 폴더 존재 확인
if not os.path.exists(source_dir):
    print(f"!!! 에러: '{source_dir}' 폴더가 없습니다.")
    print("!!! 해결방법: 'domain' 폴더 안에 'data' 폴더를 만들고 CSV 파일들을 넣어주세요.")
else:
    # 결과 폴더 생성
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 3. data 폴더 내의 모든 CSV 파일 처리
    files = [f for f in os.listdir(source_dir) if f.endswith('.csv')]
    
    if not files:
        print(f"!!! 에러: '{source_dir}' 안에 CSV 파일이 하나도 없습니다.")
    
    for filename in files:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, f"transposed_{filename}")
        
        # 파일별 skiprows 설정 (파일명에 따른 분기)
        skip = 0
        if "등록_현황" in filename or "구축현황" in filename:
            skip = 3
            
        try:
            # 데이터 로드 (한글 깨짐 방지 utf-8-sig)
            df = pd.read_csv(source_path, skiprows=skip, encoding='utf-8-sig')
            
            # 행과 열 바꾸기
            df_transposed = df.transpose().reset_index()
            
            # 저장
            df_transposed.to_csv(target_path, index=False, header=False, encoding='utf-8-sig')
            print(f"정상 변환 완료: {filename}")
            
        except Exception as e:
            print(f"오류 발생 ({filename}): {e}")

print("--- 작업 종료 ---")