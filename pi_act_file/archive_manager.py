# 📁 archive_manager.py

from paths import QUESTIONS_PATH, ARCHIVE_PATH

def archive_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as src, \
         open(ARCHIVE_PATH, "a", encoding="utf-8") as dst:
        for line in src:
            dst.write(line)

    with open(QUESTIONS_PATH, "w", encoding="utf-8") as f:
        pass

    print("📦 archive 완료 / questions.txt 초기화 ✅")

