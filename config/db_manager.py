import mysql.connector
from mysql.connector import Error
from .config import settings

class DBManager:
    """
    MySQL 데이터베이스 연결 및 쿼리 실행을 관리하는 매니저 클래스입니다.
    팀원들은 이 클래스를 직접 인스턴스화하기보다 아래의 'db' 객체 사용을 권장합니다.
    """
    
    def __init__(self):
        self.config = settings.DB_CONFIG
        self.connection = None

    def connect(self):
        """데이터베이스 연결을 생성합니다. 이미 연결되어 있다면 기존 연결을 반환합니다."""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"MySQL 연결 오류: {e}")
            return None

    def disconnect(self):
        """데이터베이스 연결을 안전하게 종료합니다."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        """
        데이터 변경(INSERT, UPDATE, DELETE) 쿼리를 실행합니다.
        성공 시 True, 실패 시 False를 반환합니다.
        """
        conn = self.connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
            return True
        except Error as e:
            print(f"쿼리 실행 오류: {e}")
            conn.rollback() # 오류 발생 시 롤백
            return False
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """
        여러 줄의 데이터를 조회(SELECT)할 때 사용합니다.
        결과를 딕셔너리 리스트([{'col1': val1, ...}, ...]) 형태로 반환합니다.
        """
        conn = self.connect()
        if not conn:
            return []
            
        cursor = conn.cursor(dictionary=True) # 컬럼명을 키로 하는 딕셔너리 반환
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"데이터 조회 오류: {e}")
            return []
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """단일 행의 데이터를 조회할 때 사용합니다. 딕셔너리 하나를 반환합니다."""
        conn = self.connect()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"데이터 단일 조회 오류: {e}")
            return None
        finally:
            cursor.close()

    # 'with' 문 사용을 위한 컨텍스트 매니저 지원
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# =================================================================
# 팀원 공용 DB 객체 (Single Instance)
# 사용법: from config import db
# 1. users = db.fetch_all("SELECT * FROM users")
# 2. db.execute_query("UPDATE users SET name=%s WHERE id=%s", ('Kim', 1))
# =================================================================
db = DBManager()
