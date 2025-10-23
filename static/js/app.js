// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    loadConfig();
    loadTokenStatus();

    // 폼 제출 이벤트
    document.getElementById('config-form').addEventListener('submit', saveConfig);

    // 토큰 상태를 주기적으로 업데이트 (30초마다)
    setInterval(loadTokenStatus, 30000);
});

// 설정 로드
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();

        if (config) {
            document.getElementById('app_url').value = config.app_url || '';
            document.getElementById('redirect_uri').value = config.redirect_uri || '';
            document.getElementById('client_id').value = config.client_id || '';
            document.getElementById('client_secret').value = config.client_secret || '';
            document.getElementById('service_key').value = config.service_key || '';
        }
    } catch (error) {
        console.error('설정 로드 실패:', error);
    }
}

// 설정 저장
async function saveConfig(e) {
    e.preventDefault();

    const config = {
        app_url: document.getElementById('app_url').value,
        redirect_uri: document.getElementById('redirect_uri').value,
        client_id: document.getElementById('client_id').value,
        client_secret: document.getElementById('client_secret').value,
        service_key: document.getElementById('service_key').value
    };

    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });

        const result = await response.json();

        showMessage('config-message', result.message, result.success ? 'success' : 'error');

        if (result.success) {
            // 단계 2 활성화
            activateStep('step-auth');
        }
    } catch (error) {
        showMessage('config-message', '설정 저장 실패: ' + error.message, 'error');
    }
}

// 인증 시작
async function startAuth() {
    try {
        showMessage('auth-message', '인증 URL을 생성하는 중...', 'info');

        const response = await fetch('/api/auth/start');
        const result = await response.json();

        if (result.success) {
            showMessage('auth-message', result.message, 'info');

            // 새 창으로 인증 URL 열기
            const authWindow = window.open(
                result.auth_url,
                'cafe24_oauth',
                'width=600,height=700,scrollbars=yes'
            );

            if (!authWindow) {
                showMessage('auth-message', '팝업이 차단되었습니다. 팝업을 허용해주세요.', 'error');
            }
        } else {
            showMessage('auth-message', result.message, 'error');
        }
    } catch (error) {
        showMessage('auth-message', '인증 시작 실패: ' + error.message, 'error');
    }
}

// 토큰 상태 로드
async function loadTokenStatus() {
    try {
        const response = await fetch('/api/token/status');
        const status = await response.json();

        const tokenStatusDiv = document.getElementById('token-status');

        if (status.has_token) {
            const badgeClass = status.is_expired ? 'expired' : 'active';
            const badgeText = status.is_expired ? '만료됨' : '활성';

            tokenStatusDiv.innerHTML = `
                <div class="status-badge ${badgeClass}">${badgeText}</div>
                <p><strong>발급 시간:</strong> ${status.issued_at}</p>
                <p><strong>만료 시간:</strong> ${new Date(status.expires_at * 1000).toLocaleString('ko-KR')}</p>
                ${!status.is_expired ? `<p><strong>남은 시간:</strong> ${status.time_remaining_formatted}</p>` : ''}
            `;

            // 단계 3 활성화
            activateStep('step-token');
        } else {
            tokenStatusDiv.innerHTML = `
                <div class="status-badge none">토큰 없음</div>
                <p>${status.message}</p>
            `;
        }
    } catch (error) {
        console.error('토큰 상태 로드 실패:', error);
        document.getElementById('token-status').innerHTML = `
            <div class="status-badge none">오류</div>
            <p>토큰 상태를 불러올 수 없습니다.</p>
        `;
    }
}

// 토큰 갱신
async function refreshToken() {
    try {
        showMessage('token-message', '토큰을 갱신하는 중...', 'info');

        const response = await fetch('/api/token/refresh', {
            method: 'POST'
        });

        const result = await response.json();

        showMessage('token-message', result.message, result.success ? 'success' : 'error');

        if (result.success) {
            loadTokenStatus();
        }
    } catch (error) {
        showMessage('token-message', '토큰 갱신 실패: ' + error.message, 'error');
    }
}

// API 테스트
async function testApi() {
    try {
        showMessage('token-message', 'API를 테스트하는 중...', 'info');

        const response = await fetch('/api/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                endpoint: '/api/v2/admin/products?limit=5'
            })
        });

        const result = await response.json();

        if (result.success) {
            showMessage('token-message', 'API 호출 성공!', 'success');

            // 결과 표시
            const apiTestSection = document.getElementById('api-test-section');
            const apiResult = document.getElementById('api-result');

            apiTestSection.style.display = 'block';
            apiResult.textContent = JSON.stringify(result.data, null, 2);

            // 결과 섹션으로 스크롤
            apiTestSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showMessage('token-message', result.message, 'error');
        }
    } catch (error) {
        showMessage('token-message', 'API 테스트 실패: ' + error.message, 'error');
    }
}

// 비밀번호 표시/숨김 토글
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    field.type = field.type === 'password' ? 'text' : 'password';
}

// 메시지 표시
function showMessage(elementId, message, type) {
    const messageDiv = document.getElementById(elementId);
    messageDiv.textContent = message;
    messageDiv.className = 'message ' + type;
    messageDiv.style.display = 'block';

    // 3초 후 자동으로 숨김 (info 메시지만)
    if (type === 'info') {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
}

// 단계 활성화
function activateStep(stepId) {
    // 모든 단계 비활성화
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });

    // 지정된 단계 활성화
    document.getElementById(stepId).classList.add('active');
}
