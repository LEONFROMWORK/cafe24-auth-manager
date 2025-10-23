# Render 배포 가이드

Cafe24 OAuth 인증 관리 툴을 Render에 무료로 배포하는 방법입니다.

## 사전 준비

1. **GitHub 계정** (코드를 업로드할 저장소)
2. **Render 계정** (https://render.com - GitHub으로 가입 가능)

## 1단계: GitHub에 코드 업로드

### 1-1. Git 저장소 초기화

```bash
cd /Users/kevin/cafe24/auth-manager

# Git 초기화
git init

# .gitignore 확인 (config.json이 포함되어 있는지 확인)
cat .gitignore

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Cafe24 OAuth Auth Manager"
```

### 1-2. GitHub 저장소 생성

1. https://github.com/new 접속
2. Repository name: `cafe24-auth-manager`
3. **Public** 또는 **Private** 선택 (무료 배포는 Public 권장)
4. **Create repository** 클릭

### 1-3. GitHub에 푸시

```bash
# GitHub 저장소 연결 (YOUR_USERNAME을 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/YOUR_USERNAME/cafe24-auth-manager.git

# 메인 브랜치로 변경
git branch -M main

# 푸시
git push -u origin main
```

## 2단계: Render에 배포

### 2-1. Render 로그인

1. https://render.com 접속
2. **GitHub으로 로그인** 또는 이메일로 가입

### 2-2. 새 Web Service 생성

1. Dashboard에서 **New +** 버튼 클릭
2. **Web Service** 선택
3. **Connect a repository** 섹션에서 GitHub 연결
4. `cafe24-auth-manager` 저장소 선택
5. **Connect** 클릭

### 2-3. 서비스 설정

다음 정보를 입력합니다:

| 항목 | 값 |
|------|-----|
| **Name** | `cafe24-auth-manager` (원하는 이름) |
| **Region** | `Singapore` (한국과 가장 가까움) |
| **Branch** | `main` |
| **Root Directory** | 비워두기 |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` |

### 2-4. 환경 변수 설정 (선택)

**Environment** 탭에서 필요시 환경 변수를 추가할 수 있습니다 (현재는 불필요).

### 2-5. 배포 시작

1. **Create Web Service** 버튼 클릭
2. 자동으로 배포 시작 (약 2-3분 소요)
3. 배포 완료되면 **Live** 상태로 변경

## 3단계: 배포된 URL 확인

배포 완료 후 상단에 다음과 같은 URL이 표시됩니다:

```
https://cafe24-auth-manager-xxxx.onrender.com
```

이 URL을 복사하세요!

## 4단계: Cafe24 앱 설정 업데이트

### 4-1. Cafe24 개발자센터 설정

1. [Cafe24 개발자센터](https://developers.cafe24.com) 접속
2. **Apps > App 관리** > 본인의 앱 선택
3. **개발 정보** 탭에서 **Redirect URI** 수정:

```
https://YOUR-APP-NAME.onrender.com/api/auth/callback
```

예시:
```
https://cafe24-auth-manager-xxxx.onrender.com/api/auth/callback
```

4. **저장** 클릭

## 5단계: 앱 사용

1. 브라우저에서 배포된 URL 접속:
   ```
   https://cafe24-auth-manager-xxxx.onrender.com
   ```

2. **앱 정보 입력**:
   - App URL
   - Redirect URI (위에서 설정한 URL)
   - Client ID
   - Client Secret
   - Service Key

3. **설정 저장** 클릭

4. **인증 시작하기** 클릭

5. Cafe24 로그인 및 권한 승인

6. 자동으로 토큰 발급 완료!

## 주의사항

### 무료 플랜 제약사항

- **자동 슬립**: 15분 동안 요청이 없으면 서버가 슬립 모드로 전환
- **재시작 시간**: 슬립 후 첫 요청 시 재시작에 30초~1분 소요
- **월 750시간**: 무료 플랜은 월 750시간만 실행 가능

### 데이터 보존

- Render의 무료 플랜은 **임시 스토리지**를 사용합니다
- `config.json` 파일은 **서버 재시작 시 삭제**될 수 있습니다
- 중요한 토큰은 따로 백업하거나 환경 변수로 관리하세요

### 해결 방법: 데이터베이스 사용 (선택)

영구 저장이 필요하면 무료 PostgreSQL이나 MongoDB를 연동할 수 있습니다.

## 문제 해결

### 배포 실패 시

**Logs** 탭에서 오류 메시지를 확인하세요.

일반적인 문제:
- Python 버전 불일치
- 패키지 설치 실패
- 포트 설정 오류

### 서버가 응답하지 않을 때

1. Render Dashboard에서 **Manual Deploy > Deploy latest commit** 클릭
2. 강제 재시작: **Manual Deploy > Clear build cache & deploy**

### 로그 확인

```bash
# Render Dashboard > Logs 탭
# 또는 CLI 사용
render logs -s cafe24-auth-manager
```

## 업데이트 배포

코드를 수정한 후 다시 배포하려면:

```bash
# 변경사항 커밋
git add .
git commit -m "Update: 변경 내용"

# GitHub에 푸시
git push origin main
```

Render가 자동으로 새 버전을 감지하고 재배포합니다!

## 비용

- **무료 플랜**: $0/월
- **제약**: 자동 슬립, 750시간/월

필요하면 업그레이드 가능:
- **Starter**: $7/월 (슬립 없음)
- **Standard**: $25/월 (더 많은 리소스)

## 추가 리소스

- [Render 공식 문서](https://render.com/docs)
- [Python 배포 가이드](https://render.com/docs/deploy-flask)
- [Render 무료 플랜 세부사항](https://render.com/pricing)

## 보안 팁

- **민감한 정보**는 절대 GitHub에 커밋하지 마세요
- `.gitignore`에 `config.json`, `.env` 포함 확인
- Client Secret 등은 Render의 **환경 변수**로 관리 가능
