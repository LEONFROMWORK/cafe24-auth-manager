#!/bin/bash

# Render CLI를 사용한 자동 배포 스크립트

echo "======================================"
echo "Cafe24 Auth Manager - Render 배포"
echo "======================================"
echo ""

# Render CLI 설치 확인
if ! command -v render &> /dev/null; then
    echo "📦 Render CLI를 설치합니다..."

    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew tap render-oss/render
            brew install render
        else
            echo "❌ Homebrew가 설치되어 있지 않습니다."
            echo "   수동으로 설치: https://render.com/docs/cli"
            exit 1
        fi
    # Linux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://render.com/install.sh | bash
    else
        echo "❌ 지원하지 않는 OS입니다."
        echo "   수동으로 설치: https://render.com/docs/cli"
        exit 1
    fi

    echo "✓ Render CLI 설치 완료"
    echo ""
fi

# Render 로그인 확인
echo "🔐 Render 로그인 확인 중..."
if ! render whoami &> /dev/null; then
    echo "Render에 로그인해주세요:"
    render login
fi

echo "✓ 로그인 완료"
echo ""

# Git 확인
if [ ! -d ".git" ]; then
    echo "📝 Git 저장소를 초기화합니다..."
    git init
    git add .
    git commit -m "Initial commit: Cafe24 OAuth Auth Manager"
    echo "✓ Git 초기화 완료"
    echo ""
fi

# GitHub 저장소 확인
if ! git remote get-url origin &> /dev/null; then
    echo "⚠️  GitHub 저장소가 연결되어 있지 않습니다."
    echo ""
    echo "다음 단계를 진행하세요:"
    echo "1. GitHub에서 새 저장소 생성: https://github.com/new"
    echo "2. 저장소 URL을 복사"
    echo "3. 다음 명령어 실행:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/cafe24-auth-manager.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    read -p "GitHub 저장소를 설정하셨나요? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# render.yaml이 있는지 확인
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml 파일이 없습니다."
    exit 1
fi

echo "🚀 Render에 배포를 시작합니다..."
echo ""

# Render 서비스 생성 및 배포
render deploy

echo ""
echo "======================================"
echo "✅ 배포 완료!"
echo "======================================"
echo ""
echo "다음 단계:"
echo "1. Render Dashboard에서 배포 상태 확인"
echo "2. 배포된 URL 복사"
echo "3. Cafe24 개발자센터에서 Redirect URI 업데이트:"
echo "   https://YOUR-APP.onrender.com/api/auth/callback"
echo ""
echo "Render Dashboard: https://dashboard.render.com"
echo "======================================"
