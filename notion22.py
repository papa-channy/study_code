import os
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

# ✅ .env에서 API 키 불러오기
load_dotenv()
notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")

# ✅ 자동 분류 함수
def classify_question(question):
    lower = question.lower()
    if any(k in lower for k in ["pandas", "데이터프레임", "groupby", "merge", "dataframe"]):
        return "Pandas"
    elif any(k in lower for k in ["시각화", "plot", "seaborn", "matplotlib"]):
        return "시각화"
    elif any(k in lower for k in ["sql", "쿼리", "join", "select", "where"]):
        return "SQL"
    else:
        return "기타"

# ✅ 질문 파일 읽기
with open("questions.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if "|" not in line:
        continue

    try:
        번호, 난이도, 데이터셋, 질문 = [part.strip() for part in line.strip().split("|", 3)]
    except ValueError:
        print(f"❌ 잘못된 형식: {line.strip()}")
        continue

    분류 = classify_question(질문)

    try:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "문제 번호": {"title": [{"text": {"content": 번호}}]},
                "난이도": {"select": {"name": 난이도}},
                "질문 내용": {"rich_text": [{"text": {"content": 질문}}]},
                "데이터셋": {"select": {"name": 데이터셋}},
                "분류": {"select": {"name": 분류}},
                "GPT 답변": {"rich_text": [{"text": {"content": ""}}]},
                "생성일자": {"date": {"start": datetime.now().isoformat()}}
            }
        )
        print(f"✅ {번호} 저장 완료 (분류: {분류})")
    except Exception as e:
        print(f"❌ {번호} 저장 실패: {e}")
