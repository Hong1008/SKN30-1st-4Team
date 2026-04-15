# 라이브러리 불러오기
import urllib.request
import json
import pandas as pd
from dotenv import load_dotenv
import os

# load_dotenv()

# key = os.getenv('bike_key')
serviceKey = "2mulQFMetApKqR%2Bx0UlbisWvmrIrEkX1pywLhQRE0ygbmrara2tM9iVQIwWH7P36nfwg%2Bmbyzsk7r9Q13KijxQ%3D%3D"
dataType = 'JSON'
pageNo = 1 #
numOfRows = 9999 # 10 - 9999

result = []
while True:

  url = f'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo?serviceKey={serviceKey}&numOfRows={numOfRows}&pageNo={pageNo}&dataType={dataType}'
  response = urllib.request.urlopen(url)
  json_str = response.read().decode('utf-8')
  # print(json_str)
  json_object = json.loads(json_str)
  result.extend(json_object['items']['item'])

  print(f'{pageNo} / {response.code} => {len(json_object['items']['item'])}')

  if len(json_object['items']['item']) <= 0 or response.code != 200 :
    break

  pageNo += 1
final = pd.json_normalize(result)

final.to_csv('ev_charger_all.csv', index=False, encoding='utf-8-sig')
print(f'저장 완료: {len(final)}행')

# print(final.info())
