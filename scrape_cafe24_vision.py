"""
Cafe24 API Documentation Scraper - OpenRouter Vision Edition
GPT-4o Vision을 사용하여 Cafe24 문서를 스크린샷으로 분석하고 OpenAPI 스펙 생성
"""
import asyncio
import json
import base64
import os
from datetime import datetime
from playwright.async_api import async_playwright
from openai import OpenAI

class VisionAPIScraper:
    def __init__(self):
        self.admin_url = "https://developers.cafe24.com/docs/api/admin/"
        self.front_url = "https://developers.cafe24.com/docs/api/front/"

        # OpenRouter API 설정
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY 환경변수를 설정해주세요")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:5001",
                "X-Title": "Cafe24 API Scraper"
            }
        )

        self.openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Cafe24 API",
                "version": "2.0",
                "description": f"Complete Cafe24 API specification (Admin + Front) - Scraped with Vision AI on {datetime.now().isoformat()}",
                "contact": {
                    "name": "Cafe24 Developers",
                    "url": "https://developers.cafe24.com"
                }
            },
            "servers": [
                {
                    "url": "https://{mallid}.cafe24api.com",
                    "description": "Cafe24 API Server",
                    "variables": {
                        "mallid": {
                            "default": "your-mall-id",
                            "description": "Your Cafe24 Mall ID"
                        }
                    }
                }
            ],
            "paths": {},
            "components": {
                "securitySchemes": {
                    "OAuth2": {
                        "type": "oauth2",
                        "flows": {
                            "authorizationCode": {
                                "authorizationUrl": "https://{mallid}.cafe24api.com/api/v2/oauth/authorize",
                                "tokenUrl": "https://{mallid}.cafe24api.com/api/v2/oauth/token",
                                "scopes": {}
                            }
                        }
                    }
                },
                "schemas": {}
            }
        }

        os.makedirs('docs/cafe24/screenshots', exist_ok=True)
        os.makedirs('docs/cafe24/specs', exist_ok=True)

    def encode_image_base64(self, image_bytes):
        """이미지를 base64로 인코딩"""
        return base64.b64encode(image_bytes).decode('utf-8')

    async def capture_screenshots(self, url, api_type):
        """페이지를 스크롤하며 섹션별로 스크린샷 캡처"""
        print(f"\n{'='*60}")
        print(f"📸 {api_type} API 스크린샷 캡처 시작: {url}")
        print(f"{'='*60}")

        screenshots = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

            print("  → 페이지 로딩 중...")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            print("  ✓ 페이지 로드 완료")

            # 전체 페이지 높이 가져오기
            total_height = await page.evaluate('document.documentElement.scrollHeight')
            viewport_height = 1080

            print(f"  → 전체 페이지 높이: {total_height}px")
            print(f"  → 뷰포트 높이: {viewport_height}px")

            # 섹션별로 스크린샷 캡처 (겹치는 부분 포함)
            current_position = 0
            screenshot_index = 0
            overlap = 100  # 100px 겹침으로 연속성 확보

            while current_position < total_height:
                # 스크롤
                await page.evaluate(f'window.scrollTo(0, {current_position})')
                await page.wait_for_timeout(1000)  # 렌더링 대기

                # 스크린샷 캡처
                screenshot_bytes = await page.screenshot(type='png')
                screenshot_path = f"docs/cafe24/screenshots/{api_type}_{screenshot_index:03d}.png"

                with open(screenshot_path, 'wb') as f:
                    f.write(screenshot_bytes)

                screenshots.append({
                    'index': screenshot_index,
                    'position': current_position,
                    'bytes': screenshot_bytes,
                    'path': screenshot_path
                })

                print(f"  ✓ 스크린샷 {screenshot_index + 1} 저장: {screenshot_path}")

                screenshot_index += 1
                current_position += (viewport_height - overlap)

            print(f"\n  ✅ 총 {len(screenshots)}개 스크린샷 캡처 완료")

            await browser.close()

        return screenshots

    async def analyze_screenshot_with_vision(self, screenshot, api_type, index, total):
        """GPT-4o Vision으로 스크린샷 분석"""
        print(f"\n  🤖 Vision AI 분석 중... ({index + 1}/{total})")

        # Base64 인코딩
        base64_image = self.encode_image_base64(screenshot['bytes'])

        # Vision API 프롬프트
        prompt = f"""You are analyzing a Cafe24 API documentation page screenshot.

Extract ALL API endpoints visible in this screenshot with the following information:

1. HTTP Method (GET, POST, PUT, DELETE, etc.)
2. API Path (e.g., /api/v2/admin/products)
3. Endpoint Title/Summary
4. Brief Description (if visible)
5. Request Parameters (name, type, required/optional, description)
6. Response Fields (name, type, description)

Return ONLY valid JSON in this exact format:
{{
  "endpoints": [
    {{
      "method": "GET",
      "path": "/api/v2/admin/products",
      "summary": "상품 목록 조회",
      "description": "쇼핑몰의 상품 목록을 조회합니다",
      "parameters": [
        {{
          "name": "shop_no",
          "in": "query",
          "type": "integer",
          "required": false,
          "description": "쇼핑몰 번호"
        }}
      ],
      "responses": {{
        "200": {{
          "description": "성공",
          "schema": {{
            "type": "object",
            "properties": {{
              "products": {{
                "type": "array",
                "description": "상품 배열"
              }}
            }}
          }}
        }}
      }}
    }}
  ]
}}

If no API endpoints are visible in this screenshot, return: {{"endpoints": []}}

IMPORTANT:
- Extract ALL visible endpoints, not just one
- Include Korean descriptions if present
- Be accurate with HTTP methods and paths
- If parameter/response details are not clearly visible, omit them rather than guessing
"""

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o",  # GPT-4o: 빠르고 저렴
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0  # 정확성을 위해 0으로 설정
            )

            # 응답 파싱
            content = response.choices[0].message.content

            # JSON 추출 (마크다운 코드 블록 제거)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)

            endpoints_count = len(result.get('endpoints', []))
            print(f"  ✅ {endpoints_count}개 엔드포인트 발견")

            # 토큰 사용량 표시
            usage = response.usage
            print(f"  💰 토큰 사용: {usage.total_tokens} (입력: {usage.prompt_tokens}, 출력: {usage.completion_tokens})")

            return result

        except Exception as e:
            print(f"  ❌ 분석 실패: {e}")
            return {"endpoints": []}

    async def scrape_with_vision(self, url, api_type):
        """Vision API로 전체 스크래핑"""
        print(f"\n{'='*60}")
        print(f"🚀 {api_type} API Vision 스크래핑 시작")
        print(f"{'='*60}")

        # 1. 스크린샷 캡처
        screenshots = await self.capture_screenshots(url, api_type)

        # 2. Vision API로 각 스크린샷 분석
        all_endpoints = []
        total_screenshots = len(screenshots)

        for i, screenshot in enumerate(screenshots):
            result = await self.analyze_screenshot_with_vision(
                screenshot, api_type, i, total_screenshots
            )

            endpoints = result.get('endpoints', [])
            all_endpoints.extend(endpoints)

            # Rate limiting 방지 (초당 1-2 요청)
            if i < total_screenshots - 1:
                print(f"  ⏳ 1초 대기 (Rate limit 방지)...")
                await asyncio.sleep(1)

        # 중복 제거 (같은 path + method)
        unique_endpoints = {}
        for ep in all_endpoints:
            key = f"{ep['method']}:{ep['path']}"
            if key not in unique_endpoints:
                unique_endpoints[key] = ep

        final_endpoints = list(unique_endpoints.values())

        print(f"\n{'='*60}")
        print(f"✅ {api_type} API 스크래핑 완료")
        print(f"  - 총 스크린샷: {total_screenshots}개")
        print(f"  - 발견된 엔드포인트: {len(all_endpoints)}개")
        print(f"  - 중복 제거 후: {len(final_endpoints)}개")
        print(f"{'='*60}")

        return final_endpoints

    def convert_to_openapi(self, endpoints):
        """추출된 엔드포인트를 OpenAPI 형식으로 변환"""
        for endpoint in endpoints:
            path = endpoint['path']
            method = endpoint['method'].lower()

            if path not in self.openapi_spec['paths']:
                self.openapi_spec['paths'][path] = {}

            # OpenAPI operation 생성
            operation = {
                "summary": endpoint.get('summary', ''),
                "description": endpoint.get('description', ''),
                "tags": [self.extract_tag_from_path(path)],
                "parameters": endpoint.get('parameters', []),
                "responses": endpoint.get('responses', {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    }
                }),
                "security": [{"OAuth2": []}]
            }

            self.openapi_spec['paths'][path][method] = operation

    def extract_tag_from_path(self, path):
        """경로에서 태그 추출"""
        parts = path.split('/')
        if len(parts) >= 5:
            return parts[4].capitalize()
        return "General"

    async def run(self):
        """전체 스크래핑 실행"""
        print("\n" + "="*60)
        print("🎨 Cafe24 API Vision Scraper")
        print("="*60)

        # Admin API 스크래핑
        admin_endpoints = await self.scrape_with_vision(self.admin_url, "admin")

        # Front API 스크래핑
        front_endpoints = await self.scrape_with_vision(self.front_url, "front")

        # OpenAPI 스펙으로 변환
        print("\n" + "="*60)
        print("🔄 OpenAPI 3.0 형식으로 변환 중...")
        print("="*60)

        all_endpoints = admin_endpoints + front_endpoints
        self.convert_to_openapi(all_endpoints)

        # 저장
        output_file = 'docs/cafe24/cafe24-openapi.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.openapi_spec, f, indent=2, ensure_ascii=False)

        # 분리된 파일로도 저장
        admin_spec = {"endpoints": admin_endpoints}
        front_spec = {"endpoints": front_endpoints}

        with open('docs/cafe24/specs/admin.json', 'w', encoding='utf-8') as f:
            json.dump(admin_spec, f, indent=2, ensure_ascii=False)

        with open('docs/cafe24/specs/front.json', 'w', encoding='utf-8') as f:
            json.dump(front_spec, f, indent=2, ensure_ascii=False)

        # 요약
        total_paths = len(self.openapi_spec['paths'])
        total_operations = sum(len(methods) for methods in self.openapi_spec['paths'].values())

        print(f"\n{'='*60}")
        print("✅ 스크래핑 완료!")
        print(f"{'='*60}")
        print(f"📊 통계:")
        print(f"  - Admin API 엔드포인트: {len(admin_endpoints)}개")
        print(f"  - Front API 엔드포인트: {len(front_endpoints)}개")
        print(f"  - 총 API 경로: {total_paths}개")
        print(f"  - 총 API 작업: {total_operations}개")
        print(f"\n💾 생성된 파일:")
        print(f"  - {output_file} (OpenAPI 3.0 전체 스펙)")
        print(f"  - docs/cafe24/specs/admin.json (Admin API)")
        print(f"  - docs/cafe24/specs/front.json (Front API)")
        print(f"  - docs/cafe24/screenshots/ (스크린샷 {len(os.listdir('docs/cafe24/screenshots'))}개)")
        print(f"{'='*60}")

async def main():
    scraper = VisionAPIScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
