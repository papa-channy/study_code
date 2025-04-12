# 📊 Notion 데이터 분석 문제 자동 관리 시스템

> 데이터 분석 스터디 / 개인 학습용 Notion + Git 자동화 시스템  
> Notion에 문제 자동 업로드, 분류, 아카이브, Git 자동 커밋/푸시까지  
> **한 큐에 자동 처리하는 통합형 CLI 관리 도구**

---

## 📌 프로젝트 소개

데이터 분석 스터디를 진행하며  
**코딩 문제를 Notion에 체계적으로 정리하고 싶다**는 생각에서 시작했습니다.  
처음에는 문제를 직접 복사해 Notion에 등록했지만  
시간이 갈수록 더 효율적인 방법이 필요했고,  
**GPT와 실시간으로 시스템을 설계하고 확장**해가며  
아래의 기능을 갖춘 완전 자동화 시스템으로 발전시켰습니다.

- ✅ **질문 문제 자동 분류 (한글 키워드 기반)**
- ✅ **Notion API로 문제 자동 업로드**
- ✅ **등록된 문제 아카이브 및 new_questions.txt 초기화**
- ✅ **Git 자동 커밋 및 푸시**
- ✅ **운영체제/브랜치명/시간 포함 커밋 메시지 자동 생성**

---

## 📂 폴더 구조

```plaintext
study_code/
├── .env                        # Notion API, DB ID 등 민감정보
├── .gitignore                  # .env 및 관리 제외 파일 설정
│
├── manage_archive/           
│   ├── classify_keywords.json  # 한글 키워드 기반 분류 규칙
│   └── archived_questions.txt  # 등록 완료된 문제 기록
│
├── python_act_file/
│   ├── notion_uploader.py      # Notion 업로드 모듈 (클래스)
│   ├── archive_manager.py      # 아카이브 관리 모듈
│   ├── run_upload.py           # 실행 스크립트 (한 번에 모든 작업)
│   └── paths.py                # 경로 관리 파일
│
├── new_questions.txt           # 등록할 문제 (양식대로)
├── requirements.txt
└── README.md

📑 문제 입력 양식
파일명: new_questions.txt

형식: 번호 | 난이도 | 데이터셋 | 문제

1 | 중 | tips | 요일별 평균 팁 금액을 구하세요.
2 | 상 | titanic | 성별별 생존율을 구하고 시각화하세요.

⚙️ 코드 실행 전 준비사항
1️⃣ .env 파일 생성
(예시)
NOTION_API_KEY=your_notion_secret_key
NOTION_DATABASE_ID=your_database_id
2️⃣ new_questions.txt에 문제 입력
3️⃣ git bash 또는 터미널에서 아래 명령 실행
bash
python python_act_file/run_upload.py

📦 Notion 데이터베이스 설정 방법
코드가 정상 동작하려면, Notion에 아래와 같은 속성을 가진 데이터베이스를 먼저 만들어두고 해당 DB의 ID를 .env에 등록해야 합니다.

속성명	타입
날짜	텍스트
문제	텍스트
dataset	Select
난이도	Select
분류	Multi-select

주의: 해당 속성 이름은 코드에서 하드코딩되어 있으므로 띄어쓰기, 대소문자까지 동일하게 작성

📊 커밋 메시지 자동화 예시
🚀 [main] 데이터 문제 추가 | 2025-04-12 20:24:00 (KST) | Windows 11
[브랜치명]사용자 입력 커밋 메시지 | KST 시간 | 운영체제 정보
자동 포함되어 Git에 푸시됩니다.

📑 프로그램 사용법

1️⃣ GPT에게 문제 생성 요청
양식:
Pandas 문제를 여러 난이도로(뒤로갈수록 어렵게),  
dataset은 seaborn 기본 예제 (iris, tips, titanic 등)별로  
3️⃣~🔟문제씩 생성해줘.  

출력 형식:  
문제번호|난이도|dataset 이름|질문 내용

조건:  
- 모든 문제는 Pandas로 해결 가능해야 함  
- 난이도: 하, 중하, 중, 중상, 상, 최상  
- 출력 형식은 꼭 '문제번호|난이도|dataset|질문 내용'
(ex) 1/1|하|tips|데이터프레임에서 전체 행 개수를 구하세요.

2️⃣ GPT 출력값을 new_questions.txt에 복사/붙여넣기

3️⃣ 터미널에서 아래 명령어 실행
bash
python python_act_file/run_upload.py
4️⃣ 성공하면

a. 문제는 Notion 데이터베이스에 저장
b. 저장한 문제는 manage_archive/archived_questions.txt로 이동
c. new_questions.txt 초기화
d. Git 커밋 메시지 입력 및 git push까지 자동화 완료

📌 제작자
papa-channy

📅 프로젝트 히스토리
2025-04-12
GPT와 실시간 협업으로 완성
Notion 자동화 + Git 커밋 자동화 시스템 구축