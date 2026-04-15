# 라이브러리 불러오기
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_gov_client

pageNo = 1
numOfRows = 10

path = '/B552584/EvCharger/getChargerInfo'
result = []
total_count = None

while True:
  params = {'numOfRows': numOfRows, 'pageNo': pageNo}
  json_object = data_gov_client._call_api(path, params)

  print(len(json_object['items']['item']))
  break

  if json_object is None:
    print(f"API 호출 최종 실패 (pageNo={pageNo}) — 수집된 {len(result)}건으로 진행합니다.")
    break

  try:
    items = json_object['items']['item']
    if total_count is None:
      total_count = json_object['totalCount']
      print(f"전체 데이터: {total_count}건")
  except (KeyError, TypeError) as e:
    print(f"응답 구조 오류: {e}")
    break

  result.extend(items)
  print(f'{pageNo} => {len(result)}/{total_count}')

  if len(result) >= total_count:
    break

  pageNo += 1

# final = pd.json_normalize(result)

# # statId 기준 중복 제거 (chgerType 숫자 기준 가장 큰 값 유지)
# final['chgerType'] = final['chgerType'].astype(int)
# final = (final.sort_values('chgerType', ascending=False)
#               .drop_duplicates(subset='statId', keep='first')
#               .reset_index(drop=True))
# print(f'중복 제거 후: {len(final)}행')

# final.to_csv('ev_charger_all_clean.csv', index=False, encoding='utf-8-sig')
# print(f'저장 완료: {len(final)}행')

# print(final.info())
