import pandas as pd
import glob
import os

# 1. 경로 지정 (r을 붙여서 경로 에러 방지)
folder_path = r'C:\Users\playdata2\Desktop\프로젝트\1차 단위 프로젝트\SKN30-1st-4Team\domain\source\한국전력공사_지역별 전기차 현황정보'
file_pattern = os.path.join(folder_path, '*.csv')
csv_files = glob.glob(file_pattern)

if not csv_files:
    print("해당 폴더에 CSV 파일이 없습니다.")
else:
    print(f"찾은 파일 개수: {len(csv_files)}개")
    
    all_df = []
    for f in csv_files:
        try:
            # 먼저 utf-8-sig로 시도
            tmp_df = pd.read_csv(f, encoding='utf-8-sig')
            all_df.append(tmp_df)
            print(f"성공 (utf-8-sig): {os.path.basename(f)}")
        except UnicodeDecodeError:
            try:
                # 실패 시 cp949(윈도우 표준 한글)로 시도
                tmp_df = pd.read_csv(f, encoding='cp949')
                all_df.append(tmp_df)
                print(f"성공 (cp949): {os.path.basename(f)}")
            except Exception as e:
                print(f"실패: {os.path.basename(f)} - 에러: {e}")

    # 4. 모든 데이터프레임을 하나로 통합
    if all_df:
        combined_df = pd.concat(all_df, ignore_index=True)
        
        # 5. 결과 확인 및 저장
        print("-" * 30)
        print("통합 완료! 전체 행 개수:", len(combined_df))
        
        output_path = os.path.join(folder_path, 'combined_car_data.csv')
        combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"파일 저장 성공: {output_path}")
    else:
        print("통합할 데이터가 없습니다.")