🏭 MES Project (Manufacturing Execution System)
이 프로젝트는 Python과 Docker를 기반으로 구축된 **생산 관리 시스템(MES)**입니다.

공정 데이터를 수집하는 SCADA 모듈과 이를 시각화 및 관리하는 웹 애플리케이션으로 구성되어 있으며, Docker Compose를 통해 데이터베이스와 애플리케이션 환경을 일괄적으로 구축하고 실행할 수 있습니다.

📂 프로젝트 구조 (Directory Structure)
Bash

Mes_project/
├── app/                 # MES 웹 애플리케이션 소스 코드 (Python/HTML)
│                        # (Flask/Django 등으로 추정되는 웹 서버 및 UI 로직)
├── scada/               # SCADA 시스템 및 데이터 수집 로직
│                        # (PLC 통신 또는 센서 데이터 시뮬레이션 코드)
├── dump/                # 데이터베이스 초기화 및 백업 파일 (.sql 등)
├── docker-compose.yml   # Docker 컨테이너 오케스트레이션 설정 파일
└── .gitignore           # Git 버전 관리 제외 목록
🛠 기술 스택 (Tech Stack)
Language: Python, HTML

Containerization: Docker, Docker Compose

Database: (docker-compose.yml에 정의된 DB, 예: MySQL/PostgreSQL)

Module: SCADA (Data Acquisition)

🚀 설치 및 실행 (Installation & Getting Started)
이 프로젝트는 Docker 환경에서 실행되도록 설계되었습니다. 실행 전 시스템에 Docker와 Docker Compose가 설치되어 있어야 합니다.

1. 저장소 클론 (Clone Repository)
Bash

git clone https://github.com/ala1012sin/Mes_project.git
cd Mes_project
2. Docker 컨테이너 실행 (Run with Docker Compose)
프로젝트 루트 디렉토리에서 아래 명령어를 실행하여 서비스를 시작합니다.

Bash

docker-compose up -d --build
참고: dump 폴더에 있는 초기 데이터가 데이터베이스 컨테이너 실행 시 자동으로 로드될 수 있습니다.

3. 서비스 접속 (Access)
컨테이너가 정상적으로 실행되면 웹 브라우저를 통해 애플리케이션에 접속할 수 있습니다.

URL: http://localhost:8000 (또는 docker-compose.yml에 설정된 포트 확인 필요)

4. 서비스 종료 (Stop)
Bash

docker-compose down
📊 주요 기능 (Features)
생산 데이터 모니터링: 웹 인터페이스를 통한 실시간 공정 현황 확인

SCADA 연동: scada 모듈을 통한 장비 데이터 수집 및 처리

데이터 관리: 생산 이력 및 설비 데이터베이스화
