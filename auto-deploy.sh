#!/bin/bash

# Cafe24 Auth Manager - 완전 자동 배포 스크립트
# GitHub 저장소 생성부터 Render 배포까지 한 번에!

set -e

echo "=========================================="
echo "🚀 Cafe24 Auth Manager 자동 배포"
echo "=========================================="
echo ""

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. GitHub CLI 설치 확인
echo -e "${BLUE}📦 1단계: 필요한 도구 확인${NC}"
echo ""

if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI를 설치합니다...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install gh
    else
        echo -e "${RED}GitHub CLI 설치가 필요합니다: https://cli.github.com${NC}"
        exit 1
    fi
fi

if ! command -v render &> /dev/null; then
    echo -e "${YELLOW}Render CLI를 설치합니다...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap render-oss/render
        brew install render
    else
        curl -fsSL https://render.com/install.sh | bash
    fi
fi

echo -e "${GREEN}✓ 도구 확인 완료${NC}"
echo ""

# 2. GitHub 로그인
echo -e "${BLUE}🔐 2단계: GitHub 인증${NC}"
echo ""

if ! gh auth status &> /dev/null; then
    echo "GitHub에 로그인해주세요..."
    gh auth login
else
    echo -e "${GREEN}✓ GitHub 로그인 완료${NC}"
fi
echo ""

# 3. Git 초기화
echo -e "${BLUE}📝 3단계: Git 저장소 초기화${NC}"
echo ""

if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: Cafe24 OAuth Auth Manager"
    echo -e "${GREEN}✓ Git 초기화 완료${NC}"
else
    echo -e "${GREEN}✓ Git 저장소 이미 존재${NC}"
fi
echo ""

# 4. GitHub 저장소 생성 및 푸시
echo -e "${BLUE}🌐 4단계: GitHub 저장소 생성${NC}"
echo ""

REPO_NAME="cafe24-auth-manager"

if ! git remote get-url origin &> /dev/null; then
    echo "GitHub 저장소를 생성합니다..."

    # 저장소 public/private 선택
    read -p "Public 저장소로 생성하시겠습니까? (무료 배포 권장) (Y/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        VISIBILITY="--private"
    else
        VISIBILITY="--public"
    fi

    # GitHub 저장소 생성
    gh repo create $REPO_NAME $VISIBILITY --source=. --remote=origin --push

    echo -e "${GREEN}✓ GitHub 저장소 생성 및 푸시 완료${NC}"
else
    echo -e "${YELLOW}저장소가 이미 연결되어 있습니다. 푸시합니다...${NC}"
    git branch -M main
    git push -u origin main
    echo -e "${GREEN}✓ 푸시 완료${NC}"
fi

# GitHub 저장소 URL 가져오기
REPO_URL=$(gh repo view --json url -q .url)
echo -e "${GREEN}저장소 URL: $REPO_URL${NC}"
echo ""

# 5. Render 로그인 및 배포
echo -e "${BLUE}☁️  5단계: Render 배포${NC}"
echo ""

if ! render whoami &> /dev/null; then
    echo "Render에 로그인해주세요..."
    render login
else
    echo -e "${GREEN}✓ Render 로그인 확인${NC}"
fi
echo ""

# Render 서비스 이름 (고유해야 함)
SERVICE_NAME="cafe24-auth-$(date +%s)"

echo "Render에 배포를 시작합니다..."
echo -e "${YELLOW}서비스 이름: $SERVICE_NAME${NC}"
echo ""

# render.yaml 기반 배포
render services create web \
    --name $SERVICE_NAME \
    --repo $REPO_URL \
    --branch main \
    --runtime python \
    --buildCommand "pip install -r requirements.txt" \
    --startCommand "gunicorn app:app" \
    --plan free \
    --region singapore

echo ""
echo -e "${GREEN}✓ Render 배포 시작!${NC}"
echo ""

# 배포 상태 확인
echo "배포 진행 상황을 확인하는 중..."
sleep 5

# 서비스 URL 가져오기 (배포 완료 후)
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 배포 프로세스 시작 완료!${NC}"
echo "=========================================="
echo ""
echo -e "${YELLOW}다음 단계:${NC}"
echo ""
echo "1. Render Dashboard 확인:"
echo "   https://dashboard.render.com"
echo ""
echo "2. 배포 완료 후 (2-3분 소요) 서비스 URL 확인"
echo ""
echo "3. Cafe24 개발자센터에서 Redirect URI 업데이트:"
echo "   https://YOUR-SERVICE.onrender.com/api/auth/callback"
echo ""
echo "4. 배포된 앱에 접속하여 인증 진행"
echo ""
echo "=========================================="
echo ""
echo "🔗 유용한 링크:"
echo "   - GitHub: $REPO_URL"
echo "   - Render: https://dashboard.render.com"
echo ""
echo "배포 로그 확인:"
echo "   render logs -s $SERVICE_NAME"
echo ""
echo "=========================================="
