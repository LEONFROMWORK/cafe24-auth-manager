# Cafe24 OAuth 인증 관리 툴

로컬에서 실행되는 웹 기반 Cafe24 API 인증 관리 도구입니다. 간단한 UI를 통해 OAuth 인증을 쉽게 완료할 수 있습니다.

## 특징

- 🎨 **직관적인 UI** - 단계별로 안내하는 웹 인터페이스
- 🔐 **자동 OAuth 인증** - 복잡한 인증 과정을 자동화
- 🎫 **토큰 관리** - Access Token 자동 갱신 및 상태 확인
- 🧪 **API 테스트** - 발급받은 토큰으로 즉시 API 테스트
- 💾 **로컬 저장** - 모든 데이터는 로컬에만 저장

## 화면 구성

1. **앱 정보 입력** - Cafe24 개발자센터에서 받은 앱 정보 입력
2. **OAuth 인증** - 원클릭으로 인증 완료
3. **토큰 관리** - 토큰 상태 확인 및 갱신, API 테스트

## 설치 및 실행

### macOS / Linux

```bash
cd auth-manager
./start.sh
```

### Windows

```bash
cd auth-manager
start.bat
```

스크립트가 자동으로 다음 작업을 수행합니다:
1. Python 버전 확인
2. 가상환경 생성 (처음 실행 시)
3. 필요한 패키지 설치
4. Flask 서버 시작
5. 브라우저 자동 실행

## 수동 실행

```bash
# 패키지 설치
pip3 install -r requirements.txt

# 서버 실행
python3 app.py
```

브라우저에서 http://localhost:5000 접속

## 사용 방법

### 1단계: 앱 정보 입력

Cafe24 개발자센터에서 생성한 앱의 정보를 입력합니다:

- **App URL**: `https://ecudemo378885.cafe24.com`
- **Redirect URI**: `https://ecudemo378885.cafe24.com/product/list.html`
- **Client ID**: 발급받은 Client ID
- **Client Secret Key**: 발급받은 Client Secret
- **Service Key**: 발급받은 Service Key

입력 후 "설정 저장" 버튼을 클릭합니다.

### 2단계: OAuth 인증

1. "인증 시작하기" 버튼 클릭
2. 새 창에서 Cafe24 로그인 및 권한 승인
3. 자동으로 토큰 발급 완료

**⚠️ 주의: 인증코드는 1분간만 유효하므로 즉시 진행하세요!**

### 3단계: 토큰 관리

인증이 완료되면 다음 작업이 가능합니다:

- **토큰 상태 확인** - 만료 시간 및 남은 시간 표시
- **토큰 갱신** - 만료 전 또는 만료 후 토큰 재발급
- **API 테스트** - 상품 목록 조회 등 실제 API 호출 테스트

## 파일 구조

```
auth-manager/
├── app.py                    # Flask 백엔드 애플리케이션
├── config.json               # 앱 설정 및 토큰 저장 (자동 생성)
├── requirements.txt          # Python 패키지 목록
├── start.sh                  # macOS/Linux 실행 스크립트
├── start.bat                 # Windows 실행 스크립트
├── templates/
│   ├── index.html           # 메인 페이지
│   └── callback.html        # OAuth 콜백 페이지
└── static/
    ├── css/
    │   └── style.css        # 스타일시트
    └── js/
        └── app.js           # 프론트엔드 JavaScript
```

## API 엔드포인트

### GET /
메인 페이지

### GET/POST /api/config
앱 설정 관리

### GET /api/auth/start
OAuth 인증 시작 (인증 URL 생성)

### GET /api/auth/callback
OAuth 콜백 처리 (토큰 발급)

### POST /api/token/refresh
Access Token 갱신

### GET /api/token/status
토큰 상태 확인

### POST /api/test
API 테스트 호출

## 환경 변수 연동

이 툴은 상위 디렉토리의 `.env` 파일과 자동으로 연동됩니다:

- 앱 정보 저장 시 `.env` 파일 자동 업데이트
- 토큰 발급 시 `.env` 파일에 저장
- 다른 스크립트에서 토큰 사용 가능

## 보안

- 모든 데이터는 로컬에만 저장됩니다
- `config.json` 파일에 앱 정보와 토큰이 저장됩니다
- 외부 서버로 데이터가 전송되지 않습니다
- `.gitignore`에 `config.json`을 추가하세요

## 문제 해결

### 포트 5000이 이미 사용 중인 경우

`app.py`의 마지막 줄을 수정:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### 브라우저가 자동으로 열리지 않는 경우

수동으로 http://localhost:5000 을 열어주세요.

### 팝업이 차단되는 경우

브라우저의 팝업 차단을 해제하거나, 주소창 오른쪽의 팝업 차단 아이콘을 클릭하여 허용하세요.

## 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: Cafe24 Admin API v2

## 라이센스

MIT

## 개발자

Cafe24 API 통합을 위한 개발 도구
