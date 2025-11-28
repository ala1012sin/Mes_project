🏭 AI-Powered MES Project (Smart Factory System)
이 프로젝트는 Python과 Docker를 기반으로 구축된 **지능형 생산 관리 시스템(MES)**입니다.

기본적인 공정 데이터 수집(SCADA) 및 관리 기능뿐만 아니라, 머신러닝/딥러닝 기반의 AI 모델을 탑재하여 생산 효율성을 극대화하고 공정 이상을 사전에 예측합니다.

특히, 고성능 연산이 필요한 모델은 서버에서, 즉각적인 반응이 필요한 시각적 분석은 웹 브라우저에서 분산 처리하는 하이브리드 AI 아키텍처를 채택했습니다.

## 📂 프로젝트 구조 (Directory Structure)

```bash
Mes_project/
├── app/                 # MES 웹 애플리케이션 & 웹 기반 AI 모델 소스
├── scada/               # SCADA 시스템 및 데이터 수집/전처리
├── dump/                # 데이터베이스 초기화 및 학습 데이터
├── docker-compose.yml   # AI 서비스 및 앱 컨테이너 오케스트레이션
└── .gitignore           # Git 설정 파일
🧠 핵심 AI 기능 (AI & Analytics)
이 시스템은 목적에 따라 Server-side와 Client-side(Web) 두 가지 환경에서 AI 모델을 구동합니다.

1. 서버 기반 예측 분석 (Server-side AI)
서버의 리소스를 활용하여 축적된 데이터를 정밀 분석하고 주요 생산 지표를 예측합니다.

📈 생산량 예측 (Production Volume Prediction): 과거 데이터를 기반으로 향후 생산량을 시계열 예측하여 재고 관리 최적화

🚚 납기 준수 여부 예측 (Delivery Compliance Prediction): 공정 현황과 리드 타임을 분석하여 납기 지연 가능성 사전 경고

⚠️ 센서 이상 감지 (Sensor Anomaly Detection): 설비 센서의 비정상 패턴을 실시간으로 감지하여 고장 예방

📉 불량률 예측 (Defect Rate Prediction): 공정 변수(온도, 압력 등)와 품질 간의 상관관계를 분석하여 불량 발생 확률 예측

2. 웹 브라우저 기반 이미지 분석 (Web-side AI)
사용자의 브라우저(Front-end)에서 경량화된 모델을 직접 구동하여 서버 부하를 줄이고 빠른 응답 속도를 제공합니다.

📷 이미지 분류 (Image Classification): 웹캠 또는 업로드된 제품 이미지를 브라우저 상에서 즉시 분석하여 제품 유형 식별 및 1차 검수 진행

🛠 기술 스택 (Tech Stack)
Language: Python, HTML/JS

AI/ML:

Server: (TensorFlow / PyTorch / Scikit-learn 등 사용된 라이브러리)

Web: (TensorFlow.js 등)

Infrastructure: Docker, Docker Compose

Database: (MySQL / PostgreSQL 등)

Module: SCADA (Data Acquisition)

🚀 설치 및 실행 (Installation)
1. 저장소 클론
Bash

git clone https://github.com/ala1012sin/Mes_project.git
cd Mes_project
2. Docker 실행
AI 모델 서버와 웹 애플리케이션, DB를 한 번에 실행합니다.

Bash

docker-compose up -d --build
3. 접속 및 모니터링
웹 대시보드: http://localhost:8000

대시보드에서 AI 예측 그래프와 실시간 이미지 분류 기능을 확인할 수 있습니다.

📊 주요 기능 (Features)
스마트 모니터링: 공정 데이터와 AI 예측 결과(생산량, 불량률 등) 시각화

SCADA 연동: 실시간 설비 데이터 수집 및 DB 적재

지능형 알림: 납기 지연 및 설비 이상 징후 포착 시 알림 제공

📝 라이선스 (License)
This project is open source.
