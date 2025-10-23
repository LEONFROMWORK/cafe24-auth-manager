#!/usr/bin/env python3
"""
Cafe24 OAuth 인증 관리 툴
로컬에서 실행되는 웹 기반 인증 관리 도구
"""

import os
import json
import time
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect
import requests
from dotenv import load_dotenv, set_key
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import base64

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'cafe24-auth-manager-secret-key'

# 환경 변수 로드
load_dotenv()

# 설정 파일 경로
CONFIG_FILE = 'config.json'
ACCOUNTS_FILE = 'accounts.json'
ENV_FILE = '../.env'

# 전역 변수로 앱 설정 저장
app_config = {}


def load_config():
    """설정 파일 로드"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    """설정 파일 저장"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def update_env_file(key, value):
    """환경 변수 파일 업데이트"""
    env_path = os.path.abspath(ENV_FILE)
    if os.path.exists(env_path):
        set_key(env_path, key, value)


def extract_shop_id(app_url):
    """App URL에서 Shop ID 추출"""
    # https://ecudemo378885.cafe24.com -> ecudemo378885
    if app_url:
        return app_url.replace('https://', '').replace('http://', '').split('.')[0]
    return ''


def load_accounts():
    """계정 목록 로드"""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return {'accounts': {}, 'current_account': None}


def save_accounts(accounts_data):
    """계정 목록 저장"""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts_data, f, indent=2, ensure_ascii=False)


def get_current_account():
    """현재 선택된 계정 가져오기"""
    accounts_data = load_accounts()
    current_id = accounts_data.get('current_account')
    if current_id and current_id in accounts_data['accounts']:
        return accounts_data['accounts'][current_id]
    return None


def save_account(shop_id, account_info):
    """계정 정보 저장"""
    accounts_data = load_accounts()
    accounts_data['accounts'][shop_id] = account_info
    if not accounts_data.get('current_account'):
        accounts_data['current_account'] = shop_id
    save_accounts(accounts_data)


def auto_refresh_tokens():
    """모든 계정의 토큰을 자동으로 갱신"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 자동 토큰 갱신 작업 시작...")

    accounts_data = load_accounts()
    if not accounts_data.get('accounts'):
        print("  → 등록된 계정이 없습니다.")
        return

    current_time = int(time.time())
    refresh_threshold = 3600  # 1시간 (3600초) 남았을 때 갱신

    for shop_id, account in accounts_data['accounts'].items():
        token = account.get('token', {})

        if not token or not token.get('refresh_token'):
            print(f"  → {shop_id}: 토큰 없음, 스킵")
            continue

        # 토큰 만료 시간 확인
        expires_at = token.get('expires_at', 0)
        try:
            expires_at = int(expires_at)
        except (ValueError, TypeError):
            expires_at = 0

        time_remaining = expires_at - current_time

        # 만료까지 1시간 미만 남았으면 갱신
        if time_remaining < refresh_threshold and time_remaining > 0:
            print(f"  → {shop_id}: 토큰 갱신 필요 (남은 시간: {time_remaining // 60}분)")

            try:
                # 토큰 갱신 API 호출
                token_url = f"https://{shop_id}.cafe24api.com/api/v2/oauth/token"

                data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': token['refresh_token']
                }

                credentials = f"{account['client_id']}:{account['client_secret']}"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()

                headers = {
                    'Authorization': f'Basic {encoded_credentials}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.post(token_url, data=data, headers=headers)
                response.raise_for_status()

                result = response.json()

                # 새 토큰으로 업데이트
                new_expires_in = result.get('expires_in', 7200)
                new_expires_at = current_time + new_expires_in

                token_data = {
                    'access_token': result['access_token'],
                    'refresh_token': result.get('refresh_token', token['refresh_token']),
                    'expires_at': new_expires_at,
                    'issued_at': datetime.now().isoformat()
                }

                account['token'] = token_data
                save_account(shop_id, account)

                print(f"  ✓ {shop_id}: 토큰 갱신 성공! (새 만료 시간: {new_expires_in // 3600}시간 후)")

            except Exception as e:
                print(f"  ✗ {shop_id}: 토큰 갱신 실패 - {str(e)}")

        elif time_remaining <= 0:
            print(f"  → {shop_id}: 토큰 만료됨, Refresh Token으로 갱신 시도")
            # 만료된 경우에도 Refresh Token이 유효하면 갱신 시도
            try:
                token_url = f"https://{shop_id}.cafe24api.com/api/v2/oauth/token"
                data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': token['refresh_token']
                }
                credentials = f"{account['client_id']}:{account['client_secret']}"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                headers = {
                    'Authorization': f'Basic {encoded_credentials}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                response = requests.post(token_url, data=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                new_expires_in = result.get('expires_in', 7200)
                new_expires_at = current_time + new_expires_in
                token_data = {
                    'access_token': result['access_token'],
                    'refresh_token': result.get('refresh_token', token['refresh_token']),
                    'expires_at': new_expires_at,
                    'issued_at': datetime.now().isoformat()
                }
                account['token'] = token_data
                save_account(shop_id, account)
                print(f"  ✓ {shop_id}: 만료된 토큰 갱신 성공!")
            except Exception as e:
                print(f"  ✗ {shop_id}: Refresh Token도 만료됨 - 재인증 필요")
        else:
            print(f"  → {shop_id}: 토큰 정상 (남은 시간: {time_remaining // 3600}시간 {(time_remaining % 3600) // 60}분)")

    print("자동 토큰 갱신 작업 완료\n")


@app.route('/')
def index():
    """메인 페이지"""
    config = load_config()
    return render_template('index.html', config=config)


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """모든 계정 목록 조회"""
    accounts_data = load_accounts()
    # 토큰 상태 계산
    for shop_id, account in accounts_data['accounts'].items():
        if account.get('token'):
            token = account['token']
            expires_at = token.get('expires_at', 0)
            try:
                expires_at = int(expires_at)
            except (ValueError, TypeError):
                expires_at = 0

            current_time = int(time.time())
            is_expired = current_time >= expires_at
            time_remaining = expires_at - current_time if not is_expired else 0

            account['token_status'] = {
                'has_token': True,
                'is_expired': is_expired,
                'expires_at': expires_at,
                'time_remaining': time_remaining,
                'time_remaining_formatted': f"{time_remaining // 3600}시간 {(time_remaining % 3600) // 60}분"
            }
        else:
            account['token_status'] = {'has_token': False}

    return jsonify(accounts_data)


@app.route('/api/accounts/switch', methods=['POST'])
def switch_account():
    """계정 전환"""
    data = request.json
    shop_id = data.get('shop_id')

    accounts_data = load_accounts()
    if shop_id in accounts_data['accounts']:
        accounts_data['current_account'] = shop_id
        save_accounts(accounts_data)
        return jsonify({'success': True, 'message': f'{shop_id} 계정으로 전환되었습니다.'})

    return jsonify({'success': False, 'message': '계정을 찾을 수 없습니다.'})


@app.route('/api/accounts/delete', methods=['POST'])
def delete_account():
    """계정 삭제"""
    data = request.json
    shop_id = data.get('shop_id')

    accounts_data = load_accounts()
    if shop_id in accounts_data['accounts']:
        del accounts_data['accounts'][shop_id]

        # 현재 계정이 삭제된 경우
        if accounts_data['current_account'] == shop_id:
            # 다른 계정이 있으면 첫 번째 계정으로 전환
            if accounts_data['accounts']:
                accounts_data['current_account'] = list(accounts_data['accounts'].keys())[0]
            else:
                accounts_data['current_account'] = None

        save_accounts(accounts_data)
        return jsonify({'success': True, 'message': f'{shop_id} 계정이 삭제되었습니다.'})

    return jsonify({'success': False, 'message': '계정을 찾을 수 없습니다.'})


@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """설정 관리 API"""
    if request.method == 'GET':
        # 현재 선택된 계정 정보 반환
        account = get_current_account()
        if account:
            return jsonify(account)
        return jsonify({})

    elif request.method == 'POST':
        data = request.json

        # Shop ID 자동 추출
        if data.get('app_url'):
            data['shop_id'] = extract_shop_id(data['app_url'])

        shop_id = data.get('shop_id')
        if not shop_id:
            return jsonify({'success': False, 'message': 'Shop ID를 추출할 수 없습니다.'})

        # 계정 정보 저장 (멀티 계정 시스템)
        save_account(shop_id, data)

        # 환경 변수 파일도 업데이트 (현재 활성 계정)
        update_env_file('CAFE24_CLIENT_ID', data.get('client_id', ''))
        update_env_file('CAFE24_CLIENT_SECRET', data.get('client_secret', ''))
        update_env_file('CAFE24_SERVICE_KEY', data.get('service_key', ''))
        update_env_file('CAFE24_SHOP_ID', shop_id)
        update_env_file('REDIRECT_URI', data.get('redirect_uri', ''))

        # 레거시 config.json도 유지 (호환성)
        save_config(data)

        return jsonify({'success': True, 'message': f'{shop_id} 계정 설정이 저장되었습니다.', 'shop_id': shop_id})


@app.route('/api/auth/start')
def start_auth():
    """인증 시작 - Authorization URL 생성"""
    account = get_current_account()

    if not account or not account.get('client_id') or not account.get('shop_id'):
        return jsonify({'success': False, 'message': '설정을 먼저 입력해주세요.'})

    config = account

    # OAuth 파라미터
    # Redirect URI: 설정에서 가져오거나 현재 호스트 기반으로 자동 생성
    redirect_uri = config.get('redirect_uri')
    if not redirect_uri:
        # 자동으로 현재 호스트 기반 redirect_uri 생성
        redirect_uri = request.host_url.rstrip('/') + '/api/auth/callback'

    # Scopes: 사용자가 선택한 권한 사용
    scopes = config.get('scopes', [])
    if not scopes:
        # 기본 scopes (앱, 상품분류, 상품 읽기/쓰기)
        scopes = [
            'mall.read_application',
            'mall.write_application',
            'mall.read_category',
            'mall.write_category',
            'mall.read_product',
            'mall.write_product'
        ]

    # scopes가 문자열이면 그대로, 리스트면 콤마로 연결
    scope_string = ','.join(scopes) if isinstance(scopes, list) else scopes

    params = {
        'response_type': 'code',
        'client_id': config['client_id'],
        'state': 'app_install',
        'redirect_uri': redirect_uri,
        'scope': scope_string
    }

    # URL 생성
    from urllib.parse import urlencode
    auth_url = f"https://{config['shop_id']}.cafe24api.com/api/v2/oauth/authorize?{urlencode(params)}"

    return jsonify({
        'success': True,
        'auth_url': auth_url,
        'message': '브라우저에서 인증을 진행해주세요.'
    })


@app.route('/api/auth/callback')
def auth_callback():
    """OAuth 콜백 처리"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    if error:
        return render_template('callback.html',
                             success=False,
                             message=f'인증 실패: {error}')

    if not code:
        return render_template('callback.html',
                             success=False,
                             message='인증 코드를 받지 못했습니다.')

    # Access Token 발급
    account = get_current_account()
    if not account:
        return render_template('callback.html',
                             success=False,
                             message='계정 정보를 찾을 수 없습니다.')

    config = account

    token_url = f"https://{config['shop_id']}.cafe24api.com/api/v2/oauth/token"

    # Redirect URI: 설정에서 가져오거나 현재 호스트 기반으로 자동 생성
    redirect_uri = config.get('redirect_uri')
    if not redirect_uri:
        redirect_uri = request.host_url.rstrip('/') + '/api/auth/callback'

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    # Authorization 헤더: Basic Auth (client_id:client_secret를 Base64 인코딩)
    import base64
    credentials = f"{config['client_id']}:{config['client_secret']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()

        result = response.json()

        # 토큰 저장
        # expires_at 계산: expires_in이 있으면 사용, 없으면 기본 2시간
        current_time = int(time.time())
        expires_in = result.get('expires_in', 7200)  # 기본 2시간
        expires_at = current_time + expires_in

        token_data = {
            'access_token': result['access_token'],
            'refresh_token': result.get('refresh_token', ''),
            'expires_at': expires_at,
            'issued_at': datetime.now().isoformat()
        }

        # 계정에 토큰 저장 (멀티 계정 시스템)
        shop_id = config['shop_id']
        account = get_current_account()
        account['token'] = token_data
        save_account(shop_id, account)

        # 레거시 config.json도 업데이트 (호환성)
        config['token'] = token_data
        save_config(config)

        # 환경 변수 파일에도 저장
        update_env_file('ACCESS_TOKEN', result['access_token'])
        update_env_file('REFRESH_TOKEN', result.get('refresh_token', ''))

        return render_template('callback.html',
                             success=True,
                             message='인증이 완료되었습니다!',
                             token_data=token_data)

    except Exception as e:
        return render_template('callback.html',
                             success=False,
                             message=f'토큰 발급 실패: {str(e)}')


@app.route('/api/token/refresh', methods=['POST'])
def refresh_token():
    """토큰 갱신"""
    account = get_current_account()

    if not account or not account.get('token', {}).get('refresh_token'):
        return jsonify({'success': False, 'message': 'Refresh Token이 없습니다.'})

    config = account
    token_url = f"https://{config['shop_id']}.cafe24api.com/api/v2/oauth/token"

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': config['token']['refresh_token']
    }

    # Authorization 헤더: Basic Auth (client_id:client_secret를 Base64 인코딩)
    import base64
    credentials = f"{config['client_id']}:{config['client_secret']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()

        result = response.json()

        # 새 토큰으로 업데이트
        # expires_at 계산: expires_in이 있으면 사용, 없으면 기본 2시간
        current_time = int(time.time())
        expires_in = result.get('expires_in', 7200)
        expires_at = current_time + expires_in

        token_data = {
            'access_token': result['access_token'],
            'refresh_token': result.get('refresh_token', config['token']['refresh_token']),
            'expires_at': expires_at,
            'issued_at': datetime.now().isoformat()
        }

        # 계정에 토큰 저장 (멀티 계정 시스템)
        shop_id = config['shop_id']
        account = get_current_account()
        account['token'] = token_data
        save_account(shop_id, account)

        # 레거시 config.json도 업데이트 (호환성)
        config['token'] = token_data
        save_config(config)

        # 환경 변수 파일에도 저장
        update_env_file('ACCESS_TOKEN', result['access_token'])
        update_env_file('REFRESH_TOKEN', result.get('refresh_token', config['token']['refresh_token']))

        return jsonify({
            'success': True,
            'message': '토큰이 갱신되었습니다.',
            'token': token_data
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'토큰 갱신 실패: {str(e)}'})


@app.route('/api/token/status')
def token_status():
    """토큰 상태 확인"""
    account = get_current_account()
    if not account:
        return jsonify({
            'has_token': False,
            'message': '계정을 선택해주세요.'
        })

    token = account.get('token', {})

    if not token:
        return jsonify({
            'has_token': False,
            'message': '토큰이 없습니다.'
        })

    expires_at = token.get('expires_at', 0)
    # expires_at이 문자열일 수 있으므로 int로 변환
    try:
        expires_at = int(expires_at)
    except (ValueError, TypeError):
        expires_at = 0

    current_time = int(time.time())
    is_expired = current_time >= expires_at
    time_remaining = expires_at - current_time if not is_expired else 0

    return jsonify({
        'has_token': True,
        'is_expired': is_expired,
        'expires_at': expires_at,
        'issued_at': token.get('issued_at', ''),
        'time_remaining': time_remaining,
        'time_remaining_formatted': f"{time_remaining // 3600}시간 {(time_remaining % 3600) // 60}분"
    })


@app.route('/api/test', methods=['POST'])
def test_api():
    """API 테스트"""
    account = get_current_account()
    if not account:
        return jsonify({'success': False, 'message': '계정을 선택해주세요.'})

    config = account
    token = config.get('token', {})

    if not token.get('access_token'):
        return jsonify({'success': False, 'message': 'Access Token이 없습니다.'})

    endpoint = request.json.get('endpoint', '/api/v2/admin/products')

    url = f"https://{config['shop_id']}.cafe24api.com{endpoint}"

    headers = {
        'Authorization': f"Bearer {token['access_token']}",
        'Content-Type': 'application/json',
        'X-Cafe24-Api-Version': '2025-09-01',
        'X-Cafe24-Client-Id': config['client_id']
    }

    try:
        # 디버깅: 요청 정보 로깅
        print(f"API Test Request:")
        print(f"  URL: {url}")
        print(f"  Headers: {headers}")

        response = requests.get(url, headers=headers)

        # 디버깅: 응답 정보 로깅
        print(f"  Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"  Response Body: {response.text}")

        response.raise_for_status()

        return jsonify({
            'success': True,
            'status_code': response.status_code,
            'data': response.json()
        })

    except Exception as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = f"{str(e)} - Response: {e.response.text}"
            except:
                pass

        return jsonify({
            'success': False,
            'message': f'API 호출 실패: {error_detail}',
            'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        })


# 자동 토큰 갱신 스케줄러 초기화
scheduler = BackgroundScheduler()
scheduler.add_job(func=auto_refresh_tokens, trigger="interval", hours=1)  # 1시간마다 실행
scheduler.start()

# 앱 종료 시 스케줄러도 종료
atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    import os

    # 로컬 개발 모드 확인
    is_local = os.environ.get('FLASK_ENV') == 'development' or not os.environ.get('RENDER')

    if is_local:
        print('=' * 80)
        print('Cafe24 OAuth 인증 관리 툴')
        print('=' * 80)
        print()
        print('브라우저에서 http://localhost:5001 을 열어주세요.')
        print()
        print('🔄 자동 토큰 갱신 기능 활성화 (1시간마다 체크)')
        print()
        print('종료하려면 Ctrl+C를 누르세요.')
        print('=' * 80)
        print()

        # 자동으로 브라우저 열기
        webbrowser.open('http://localhost:5001')

    # Flask 앱 실행
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=is_local)
