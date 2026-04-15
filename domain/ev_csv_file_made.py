import pandas as pd
import os
import xlrd

# 1. 파일이 위치한 정확한 경로 설정
base_path = 'domain/src_raw'

# 2. 변환할 파일 리스트
target_files = [
    '201001_202510_지역별_전기차_충전기_구축현황(누적).xls',
    '201001_202512_지역별_전기차_등록_현황(누적).xls'
]

for file_name in target_files:
    # 전체 경로 생성
    xls_path = os.path.join(base_path, file_name)
    csv_path = os.path.join(base_path, file_name.replace('.xls', '.csv'))
    
    try:
        # 3. xls 파일 읽기 (구형 엑셀 엔진 xlrd 사용)
        df = pd.read_excel(xls_path, engine='xlrd')
        
        # 4. csv 파일로 저장 (한글 깨짐 방지 utf-8-sig)
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ 변환 완료: {csv_path}")
        
    except Exception as e:
        print(f"❌ {file_name} 변환 중 에러 발생: {e}")

print("-" * 30)
print("모든 작업이 완료되었습니다.")