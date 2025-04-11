#!/bin/bash

# 🌍 현재 시간 (KST 기준)
current_time=$(TZ=Asia/Seoul date "+%Y-%m-%d %H:%M:%S")

# 🌱 현재 브랜치
branch=$(git rev-parse --abbrev-ref HEAD)

# 💻 운영체제 및 버전 감지
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        os_type="$NAME $VERSION"
    else
        os_type="Linux (Unknown Version)"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    os_type="macOS $(sw_vers -productVersion)"
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    if command -v systeminfo &> /dev/null; then
        win_version=$(systeminfo | grep -E "^OS Name|^OS Version" | tr '\n' ' ' | sed 's/^.*OS Name: //; s/ OS Version:/ \(/; s/$/\)/')
        os_type="Windows $win_version"
    else
        os_type="Windows (Version Unknown)"
    fi
else
    os_type="Unknown OS"
fi

# 🔍 변경된 파일들 미리 보여주기
echo "🔍 변경된 파일:"
git status -s
echo ""

# 📝 커밋 메시지 받기 (Python에서 전달받거나 fallback)
if [ -z "$COMMIT_MSG" ]; then
    read -p "📝 커밋 메시지를 입력하세요 (비워두면 '자동 커밋'): " user_message
    if [ -z "$user_message" ]; then
        user_message="자동 커밋"
    fi
else
    user_message="$COMMIT_MSG"
fi

# 📦 최종 커밋 메시지
commit_message="🚀 [$branch] $user_message | $current_time (KST) | $os_type"

# Git 명령어 실행
git add .
git commit -m "$commit_message"
git push

echo ""
echo "✅ 커밋 완료!"
echo "$commit_message"