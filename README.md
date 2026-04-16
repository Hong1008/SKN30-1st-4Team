# 🔌 전기차 충전 인프라 대시보드 (SKN30-1st-4Team)

전국 전기차 등록 현황 대비 충전 인프라 공급량을 분석하여, 충전이 가장 불편한 'SOS 핫스팟'을 시각화하는 프로젝트입니다.
---

## 🛠️ 기술 스택 (Tech Stack)

### 📊 Frontend & Visualization
- **Streamlit**: 대시보드 웹 UI 프레임워크
- **Plotly**: 반응형 멀티태스킹 데이터 차트 생성
- **Folium**: 지리 공간 데이터 시각화 (핫스팟 분석)

### 🧠 Backend & Data Processing
- **Python 3**: 메인 프로그래밍 언어
- **Pandas**: 데이터 로드 및 전처리 (CSV 등)
- **Pandera**: DataFrame 스키마 검증 및 데이터 안정성 확보
- **Mysql**: 통계 및 메타데이터 저장

### ⚙️ Environment & Tools
- **uv**: 파이썬 의존성 및 패키지 관리
- **Git & GitHub**: 형상 관리 및 팀 협업

---

## 📂 프로젝트 구조 (Folder Structure)

```bash
🚘 SKN30-1st-4Team/
├── ⚙️ config/                # 설정 및 공통 모듈
│   ├── config.py             # 환경 변수 로드 및 전역 설정
│   ├── db_manager.py         # MySQL 연결 및 쿼리 실행
│   └── __init__.py           # 패키지 노출 설정
├── 🧠 domain/                # 비즈니스 로직 및 데이터 처리
│   ├── ev_service.py         # 데이터 전처리 및 분석 프레임워크
│   ├── load_by_csv.py        # CSV 기반 데이터 로드 및 불편 지수(TCII) 산출
│   ├── load_by_db.py         # DB 기반 데이터 파이프라인
│   ├── ev_schema.py          # 데이터 스키마 정의 (Pandera)
│   ├── crawling/             # 외부 크롤링 스크립트
│   ├── src_raw/              # 수집한 원본 데이터
│   ├── src_clean/            # 분석용 1차 정제 데이터
│   └── sql/                  # DB 테이블 쿼리문
├── 🎨 web/                   # Streamlit UI 컴포넌트
│   ├── view.py               # UI 메인 레이아웃 및 탭 제어
│   ├── section_map.py        # 지도 시각화 (핫스팟)
│   ├── section_comparison_chart.py  # 수요-공급 현황 비교 바 차트
│   ├── section_line_chart.py # 연도별/지역별 동향 라인 차트
│   ├── section_data_table.py # 상세 데이터 표 및 CSV 다운로드
│   ├── section_wordcloud.py  # 키워드 워드 클라우드
├── 📄 docs/                  # 프로젝트 문서
├── 🚀 Root Files
│   ├── main.py               # 대시보드 메인 실행 파일
│   ├── .env                  # 환경 변수 보안 설정 (Git 제외)
│   ├── pyproject.toml        # 의존성 관리 설정 (uv)
│   └── README.md             # 프로젝트 개요 및 가이드
```

---

## 🛠️ 개발 환경 설정

이 프로젝트는 `uv`를 활용하여 패키지를 관리합니다.

```bash
# 의존성 설치 및 실행
uv sync
.venv\bin\activate
uv run streamlit run main.py
```

---

## 🌿 브랜치 전략 (Git Strategy)

팀 프로젝트의 안정적인 협업을 위해 아래의 브랜치 전략을 따릅니다.

1. **`main`**: 상용 서비스가 배포되는 기준 브랜치입니다. 모든 기능 개발이 완료되고 검증된 코드만 병합합니다.
2. **`feat/`**: 새로운 기능 개발 또는 개별 작업을 위한 개발 브랜치입니다.
   - 브랜치 생성 규칙: `feat/본인작업명` (예: `feat/api-client`, `feat/map-v1`)
3. **협업 흐름**:
   - `main` 브랜치에서 본인의 작업을 위한 `feat/작업명` 브랜치를 생성합니다.
   - 작업이 완료되면 `main` 브랜치로 **Pull Request (PR)**를 요청합니다.
   - 코드 리뷰 또는 팀원 간 합의 후 `main`에 병합(Merge)합니다.
