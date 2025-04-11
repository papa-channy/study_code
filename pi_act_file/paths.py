# 📁 paths.py
import os

# 현재 파일 기준 최상위 디렉토리 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 아카이브 질문 파일 경로
ARCHIVE_PATH = os.path.join(BASE_DIR, "../manage_archive/archived_questions.txt")

# 키워드 분류 기준 JSON 경로
KEYWORDS_PATH = os.path.join(BASE_DIR, "../manage_archive/classify_keywords.json")

# 질문 입력 파일 경로 (필요시)
QUESTIONS_PATH = os.path.join(BASE_DIR, "../new_questions.txt")

# Notion DB ID 및 API Key는 .env 파일에서 불러옴
# .env 파일은 프로젝트 루트 디렉토리에 위치해야 함 
ENV_PATH = os.path.join(BASE_DIR, "../.env")