# 🚀 빠른 시작 가이드

## 완전 자동 배포 (1분!)

단 한 줄의 명령어로 GitHub 저장소 생성부터 Render 배포까지 자동으로 진행됩니다.

```bash
cd /Users/kevin/cafe24/auth-manager
./auto-deploy.sh
```

### 자동으로 수행되는 작업

1. ✅ GitHub CLI 및 Render CLI 설치 (필요시)
2. ✅ GitHub 로그인 (처음 한 번만)
3. ✅ Git 저장소 초기화
4. ✅ GitHub 저장소 자동 생성
5. ✅ 코드 자동 푸시
6. ✅ Render에 자동 배포

### 필요한 것

- **GitHub 계정** (무료)
- **Render 계정** (무료)

## 단계별 진행

### 1. 스크립트 실행

```bash
./auto-deploy.sh
```

### 2. 대화형 질문에 답변

#### GitHub 로그인 (처음 실행 시)
```
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser
```

브라우저가 열리면 로그인하고 승인합니다.

#### 저장소 공개 여부
```
Public 저장소로 생성하시겠습니까? (무료 배포 권장) (Y/n):
```

**Y** 입력 (무료 배포는 Public 저장소 권장)

#### Render 로그인 (처음 실행 시)
```
Visit https://dashboard.render.com/... to authenticate
```

브라우저에서 Render에 로그인하고 승인합니다.

### 3. 배포 완료 대기

스크립트가 자동으로:
- GitHub 저장소 생성
- 코드 푸시
- Render 배포 시작

**2-3분** 후 배포가 완료됩니다!

### 4. 배포된 URL 확인

배포 완료 후 Render Dashboard에서 URL을 확인:
```
https://dashboard.render.com
```

서비스를 클릭하면 상단에 URL이 표시됩니다:
```
https://cafe24-auth-xxxx.onrender.com
```

### 5. Cafe24 설정 업데이트

[Cafe24 개발자센터](https://developers.cafe24.com)에서:

1. **Apps > App 관리** > 본인 앱 선택
2. **개발 정보** > **Redirect URI** 추가:
   ```
   https://cafe24-auth-xxxx.onrender.com/api/auth/callback
   ```
3. **저장**

### 6. 앱 사용 시작!

배포된 URL로 접속:
```
https://cafe24-auth-xxxx.onrender.com
```

1. 앱 정보 입력
2. 인증 시작하기
3. 토큰 자동 발급 완료!

## 문제 해결

### GitHub CLI가 설치되지 않는 경우

```bash
# macOS
brew install gh

# 다른 OS
# https://cli.github.com 에서 설치
```

### Render CLI가 설치되지 않는 경우

```bash
# macOS
brew tap render-oss/render
brew install render

# Linux
curl -fsSL https://render.com/install.sh | bash
```

### 배포 실패 시

Render Dashboard의 **Logs** 탭에서 오류를 확인하세요:
```
https://dashboard.render.com
```

### 수동 배포

자동화 스크립트 없이 수동으로 배포하려면 `DEPLOY.md`를 참고하세요.

## 유용한 명령어

```bash
# 배포 로그 확인
render logs -s cafe24-auth-xxxx

# 서비스 재시작
render services restart cafe24-auth-xxxx

# 서비스 상태 확인
render services list

# 서비스 삭제
render services delete cafe24-auth-xxxx
```

## 비용

**완전 무료!**

- GitHub: 무료 Public 저장소
- Render: 무료 플랜 (750시간/월)

## 다음 단계

배포가 완료되면:

1. 배포된 앱에서 Cafe24 앱 정보 입력
2. OAuth 인증 완료
3. 토큰 관리 및 API 테스트

행운을 빕니다! 🎉
