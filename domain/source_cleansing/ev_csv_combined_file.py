import pandas as pd
import glob
import os

# 1. 경로 지정
folder_path = r'C:\Users\playdata2\Desktop\프로젝트\1차 단위 프로젝트\SKN30-1st-4Team\domain\source\한국전력공사_지역별 전기차 현황정보'
file_pattern = os.path.join(folder_path, '*.csv')
csv_files = glob.glob(file_pattern)

if not csv_files:
    print("해당 폴더에 CSV 파일이 없습니다.")
else:
    all_df = []
    for f in csv_files:
        try:
            tmp_df = pd.read_csv(f, encoding='utf-8-sig')
            all_df.append(tmp_df)
        except UnicodeDecodeError:
            tmp_df = pd.read_csv(f, encoding='cp949')
            all_df.append(tmp_df)

    if all_df:
        # 4. 데이터프레임 통합
        combined_df = pd.concat(all_df, ignore_index=True)
        
        # [추가] 중복 제거 로직 시작
        # 1) 기준일을 데이트타임 형식으로 변환
        combined_df['기준일'] = pd.to_datetime(combined_df['기준일'])
        
        # 2) 날짜 순으로 정렬 (최신 데이터를 남기거나 처음 데이터를 남기기 위해 필수)
        combined_df = combined_df.sort_values('기준일')
        
        # 3) 년도와 월이 같으면 중복으로 처리하기 위해 임시 컬럼 생성
        combined_df['년월'] = combined_df['기준일'].dt.to_period('M')
        
        # 4) '년월'이 중복되는 행 중 첫 번째만 남기고 삭제
        before_count = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['년월'], keep='first')
        after_count = len(combined_df)
        
        # 임시 컬럼 삭제 및 다시 날짜순 정렬
        combined_df = combined_df.drop(columns=['년월']).sort_values('기준일')
        
        # 5. 결과 확인 및 저장
        print("-" * 30)
        print(f"중복 제거 완료: {before_count}행 -> {after_count}행 ({before_count - after_count}개 삭제)")
        
        output_path = os.path.join(folder_path, 'combined_car_data.csv')
        combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"파일 저장 성공: {output_path}")