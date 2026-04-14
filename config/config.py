# =================================================================
# 프로젝트 전역 설정 관리 모듈
# 팀원 필독: .env 파일에 DB 연결 정보를 반드시 설정해야 합니다.
# =================================================================

import os
from dotenv import load_dotenv
from pathlib import Path

# 1. 프로젝트 루트 경로 설정 (프로젝트 어느 위치에서든 .env를 찾기 위함)
# Path(__file__)는 이 파일(config.py)의 위치를 의미합니다.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'

# 2. .env 파일 로드 (DB_HOST, DB_USER 등의 환경변수 활성화)
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv() # 기본 .env 로드 시도

# 3. 데이터베이스 연결 설정 (os.getenv를 통해 보안 유지)
# 팀원 가이드: 자신의 .env 파일에 아래 키값들을 추가하세요.
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'practice_db'),
    'connection_timeout': 10
}

# 4. 공공 데이터 API 설정
DATA_GOV_URL = os.getenv('DATA_GOV_URL', 'http://apis.data.go.kr')
DATA_GOV_SERVICE_KEY = os.getenv('DATA_GOV_SERVICE_KEY')
