# 📁 run_upload.py
import subprocess
import os
import platform
from datetime import datetime
from notion_uploader import Notion_Uploader
from archive_manager import archive_questions

print("🚀 Notion 업로드 시작")
uploader = Notion_Uploader()
uploader.upload()

print("\n🗂 아카이빙 시작")
archive_questions()
print("✅ 아카이빙 완료")

print("\n🛠 Git 자동 배포 시작...")

# 1️⃣ 현재 시간 (KST 기준)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 2️⃣ 현재 브랜치명
try:
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        stderr=subprocess.STDOUT
    ).decode().strip()
except subprocess.CalledProcessError:
    branch = "unknown"

# 3️⃣ 운영체제 및 버전 감지
system = platform.system()
if system == "Linux":
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
            name = ""
            version = ""
            for line in lines:
                if line.startswith("NAME="):
                    name = line.strip().split("=")[1].strip('"')
                elif line.startswith("VERSION="):
                    version = line.strip().split("=")[1].strip('"')
            os_type = f"{name} {version}"
    except Exception:
        os_type = "Linux (Unknown Version)"
elif system == "Darwin":
    os_type = f"macOS {platform.mac_ver()[0]}"
elif system == "Windows":
    try:
        output = subprocess.check_output("systeminfo", shell=True).decode("cp949", errors="ignore")
        os_name = ""
        os_version = ""
        for line in output.splitlines():
            if line.startswith("OS Name"):
                os_name = line.split(":", 1)[1].strip()
            elif line.startswith("OS Version"):
                os_version = line.split(":", 1)[1].strip()
        os_type = f"{os_name} ({os_version})"
    except Exception:
        os_type = "Windows (Version Unknown)"
else:
    os_type = "Unknown OS"

# 4️⃣ 변경된 파일 미리 보여주기
print("\n🔍 변경된 파일:")
subprocess.run(["git", "status", "-s"])

# 5️⃣ 커밋 메시지 입력
user_msg = input("\n📝 커밋 메시지를 입력하세요 (비워두면 '자동 커밋'): ")
if not user_msg.strip():
    user_msg = "자동 커밋"

# 6️⃣ 최종 커밋 메시지
commit_msg = f"🚀 [{branch}] {user_msg} | {now} (KST) | {os_type}"

# 7️⃣ Git 명령어 실행
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"\n✅ 커밋 완료!\n📦 {commit_msg}")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Git 작업 실패: {e}")
