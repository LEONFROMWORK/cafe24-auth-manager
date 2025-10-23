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

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'cafe24-auth-manager-secret-key'

# 환경 변수 로드
load_dotenv()

# 설정 파일 경로
CONFIG_FILE = 'config.json'
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


@app.route('/')
def index():
    """메인 페이지"""
    config = load_config()
    return render_template('index.html', config=config)


@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """설정 관리 API"""
    if request.method == 'GET':
        config = load_config()
        return jsonify(config)

    elif request.method == 'POST':
        data = request.json

        # Shop ID 자동 추출
        if data.get('app_url'):
            data['shop_id'] = extract_shop_id(data['app_url'])

        # 설정 저장
        save_config(data)

        # 환경 변수 파일도 업데이트
        update_env_file('CAFE24_CLIENT_ID', data.get('client_id', ''))
        update_env_file('CAFE24_CLIENT_SECRET', data.get('client_secret', ''))
        update_env_file('CAFE24_SERVICE_KEY', data.get('service_key', ''))
        update_env_file('CAFE24_SHOP_ID', data.get('shop_id', ''))
        update_env_file('REDIRECT_URI', data.get('redirect_uri', ''))

        # 전역 변수에도 저장
        global app_config
        app_config = data

        return jsonify({'success': True, 'message': '설정이 저장되었습니다.'})


@app.route('/api/auth/start')
def start_auth():
    """인증 시작 - Authorization URL 생성"""
    config = load_config()

    if not config.get('client_id') or not config.get('shop_id'):
        return jsonify({'success': False, 'message': '설정을 먼저 입력해주세요.'})

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
    config = load_config()

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

        # 설정 파일에 토큰 추가
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
    config = load_config()

    if not config.get('token', {}).get('refresh_token'):
        return jsonify({'success': False, 'message': 'Refresh Token이 없습니다.'})

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
    config = load_config()
    token = config.get('token', {})

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
    config = load_config()
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
        print('종료하려면 Ctrl+C를 누르세요.')
        print('=' * 80)
        print()

        # 자동으로 브라우저 열기
        webbrowser.open('http://localhost:5001')

    # Flask 앱 실행
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=is_local)
