@echo off
chcp 65001 > nul

echo ======================================
echo Cafe24 OAuth 인증 관리 툴
echo ======================================
echo.

REM Python 버전 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3가 설치되어 있지 않습니다.
    echo    Python 3.7 이상을 설치해주세요.
    pause
    exit /b 1
)

echo ✓ Python 설치 확인 완료
echo.

REM 가상환경 확인 및 생성
if not exist "venv" (
    echo 📦 가상환경을 생성하는 중...
    python -m venv venv
    echo ✓ 가상환경이 생성되었습니다.
    echo.
)

REM 가상환경 활성화
echo 🔄 가상환경을 활성화하는 중...
call venv\Scripts\activate.bat

REM 패키지 설치
echo 📥 필요한 패키지를 설치하는 중...
pip install -q -r requirements.txt

echo ✓ 패키지 설치 완료
echo.

REM Flask 앱 실행
echo 🚀 서버를 시작합니다...
echo.
echo 브라우저에서 다음 주소로 접속하세요:
echo 👉 http://localhost:5000
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo ======================================
echo.

python app.py
