import os
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

# ✅ .env에서 API 키 불러오기
load_dotenv()
notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")

print("✅ Notion API Key:", os.getenv("NOTION_API_KEY")[:10], "...")
print("✅ Notion DB ID:", os.getenv("NOTION_DATABASE_ID"))

# ✅ 다중 분류 감지 함수
def classify_question_multi(question):
    lower = question.lower()
    tags = []

    if any(k in lower for k in ["pandas", "데이터프레임", "groupby", "merge", "dataframe"]):
        tags.append("Pandas")
    if any(k in lower for k in ["시각화", "plot", "seaborn", "matplotlib"]):
        tags.append("시각화")
    if any(k in lower for k in ["sql", "쿼리", "join", "select", "where"]):
        tags.append("SQL")

    if not tags:
        tags.append("기타")

    return tags

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

    분류_목록 = classify_question_multi(질문)

    try:
        #today_pretty = datetime.now().strftime("%-m/%-d")  # mac/Linux
        today_pretty = datetime.now().strftime("%#m/%#d")  # Windows용이면 이거 사용
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "날짜": {"rich_text": [{"text": {"content": today_pretty}}]},
                "dataset": {"select": {"name": 데이터셋}},
                "문제": {"rich_text": [{"text": {"content": 질문}}]},
                "분류": {"multi_select": [{"name": tag} for tag in 분류_목록]},
                "난이도": {"select": {"name": 난이도}},
            }
        )
        print(f"✅ {번호} 저장 완료 (분류: {', '.join(분류_목록)})")
    except Exception as e:
        print(f"❌ {번호} 저장 실패: {e}")
