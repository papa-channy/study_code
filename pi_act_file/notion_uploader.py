# 📁 notion_uploader.py
# 📦 Notion API를 사용하여 문제를 업로드하는 스크립트입니다.
import os
import json
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime
from paths import KEYWORDS_PATH, QUESTIONS_PATH, ENV_PATH
class Notion_Uploader:
    def __init__(self):
        self.question_file = QUESTIONS_PATH
        self.keyword_map = self.load_keyword_map(KEYWORDS_PATH)
        
        # 🛠️ .env에서 API 키 불러오기
        load_dotenv(dotenv_path=ENV_PATH)
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        # print("🔐 Notion API Key:", os.getenv("NOTION_API_KEY")[:10], "...")
        # print("📦 Notion DB ID:", os.getenv("NOTION_DATABASE_ID"))
    
    # 📚 분류 키워드 JSON 로드
    def load_keyword_map(self, filepath): #filepath="classify_keywords.json"
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
        
    # 🧠 한글 키워드 기반 자동 분류 함수
    def classify(self, text):
        categories = []
        for category, keywords in self.keyword_map.items():
            if any(k in text for k in keywords):
                categories.append(category)
        return list(set(categories))    # 키워드 없으면 빈 리스트 반환 
    
    # 📂 질문 파일 읽기
    def upload(self):
        with open(self.question_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 🚀 한 줄씩 문제 등록    
        for line in lines:
            if "|" not in line:
                continue

            # 📌 분류 자동 감지
            try:
                번호, 난이도, 데이터셋, 질문 = [part.strip() for part in line.strip().split("|", 3)]
            except ValueError:
                print(f"❌ 잘못된 형식: {line.strip()}")
                continue

            분류_목록 = self.classify(질문)

            try:
                today = datetime.now().strftime("%#m/%#d")
                self.notion.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "날짜": {"rich_text": [{"text": {"content": today}}]},
                        "dataset": {"select": {"name": 데이터셋}},
                        "문제": {"rich_text": [{"text": {"content": 질문}}]},
                        "분류": {"multi_select": [{"name": tag} for tag in 분류_목록]} if 분류_목록 else {},
                        "난이도": {"select": {"name": 난이도}},
                    }
                )
                print(f"✅ {번호} 저장 완료 | 분류: {', '.join(분류_목록) if 분류_목록 else '없음'}")
            except Exception as e:
                print(f"❌ {번호} 저장 실패: {e}")

