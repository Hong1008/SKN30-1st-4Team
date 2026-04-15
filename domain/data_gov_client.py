import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
from typing import Optional, Dict
from config.config import settings

def _call_api(path: str, params: Dict) -> Optional[Dict]:
    """
    공공데이터 API를 호출하는 공통 함수입니다. 이 파일 내부에서만 사용합니다.

    Args:
        path (str): API 엔드포인트 경로 (예: '/B552584/EvCharger/getChargerStatus')
        params (dict): 요청 파라미터 딕셔너리

    Returns:
        Optional[Dict]: 호출 성공 시 JSON 응답 데이터, 실패 시 None
    """
    # 1. URL 구성
    # URL이 '/'로 시작하지 않을 경우를 대비해 처리
    if not path.startswith('/'):
        path = '/' + path

    # url = f"{DATA_GOV_URL}{path}"

    url = f"{settings.DATA_GOV_URL}{path}"

    # 2. 필수 기본 파라미터 추가
    # 서비스키는 .env에서 가져온 값을 사용하며, JSON 형식을 기본으로 요청합니다.
    api_params = params.copy()
    if 'serviceKey' not in api_params and 'ServiceKey' not in api_params:
        # api_params['serviceKey'] = DATA_GOV_SERVICE_KEY

       api_params['serviceKey'] = settings.DATA_GOV_SERVICE_KEY

    if 'dataType' not in api_params:
        api_params['dataType'] = 'JSON'

    try:
        # 3. API 호출
        response = requests.get(url, params=api_params)

        # 4. 응답 상태 확인
        response.raise_for_status()

        # 5. 데이터 반환
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"API 호출 중 오류 발생 (URL: {url}): {e}")
        return None
    except ValueError as e:
        print(f"JSON 파싱 오류: {e}")
        return None
