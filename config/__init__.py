# =================================================================
# config 패키지 초기화 파일
# from config import db 으로 DB 객체를 가져올 수 있습니다.
# =================================================================

from .config import DB_CONFIG
from .db_manager import db

__all__ = ['DB_CONFIG', 'db']
