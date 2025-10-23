"""
Cafe24 API 검증 및 카테고리화
1. 추출된 데이터 품질 검증
2. 카테고리별 분류
3. 구조화된 문서 생성
"""
import json
import re
from collections import defaultdict
from pathlib import Path

class APIVerifier:
    def __init__(self):
        self.admin_file = "docs/cafe24/specs/admin.json"
        self.front_file = "docs/cafe24/specs/front.json"
        self.openapi_file = "docs/cafe24/cafe24-openapi.json"

    def load_data(self):
        """데이터 로드"""
        with open(self.admin_file, 'r', encoding='utf-8') as f:
            self.admin_data = json.load(f)

        with open(self.front_file, 'r', encoding='utf-8') as f:
            self.front_data = json.load(f)

        with open(self.openapi_file, 'r', encoding='utf-8') as f:
            self.openapi_data = json.load(f)

    def verify_data_quality(self):
        """데이터 품질 검증"""
        print("\n" + "="*60)
        print("📊 데이터 품질 검증")
        print("="*60)

        admin_endpoints = self.admin_data['endpoints']
        front_endpoints = self.front_data['endpoints']

        # 1. 기본 통계
        print(f"\n1️⃣ 기본 통계:")
        print(f"  - Admin API 엔드포인트: {len(admin_endpoints)}개")
        print(f"  - Front API 엔드포인트: {len(front_endpoints)}개")
        print(f"  - OpenAPI 경로: {len(self.openapi_data['paths'])}개")

        # 2. 완전성 검증
        print(f"\n2️⃣ 데이터 완전성:")
        complete_endpoints = []
        incomplete_endpoints = []

        for ep in admin_endpoints + front_endpoints:
            required_fields = ['method', 'path', 'summary']
            if all(field in ep and ep[field] for field in required_fields):
                complete_endpoints.append(ep)
            else:
                incomplete_endpoints.append(ep)

        print(f"  - 완전한 데이터: {len(complete_endpoints)}개 ({len(complete_endpoints)/(len(admin_endpoints)+len(front_endpoints))*100:.1f}%)")
        print(f"  - 불완전한 데이터: {len(incomplete_endpoints)}개")

        if incomplete_endpoints[:3]:
            print(f"\n  불완전한 데이터 샘플:")
            for ep in incomplete_endpoints[:3]:
                print(f"    - {ep.get('method', 'N/A')} {ep.get('path', 'N/A')}: {ep.get('summary', 'N/A')}")

        # 3. HTTP 메서드 분포
        print(f"\n3️⃣ HTTP 메서드 분포:")
        method_counts = defaultdict(int)
        for ep in admin_endpoints + front_endpoints:
            method_counts[ep.get('method', 'UNKNOWN')] += 1

        for method, count in sorted(method_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {method}: {count}개")

        # 4. 경로 패턴 분석
        print(f"\n4️⃣ 주요 API 카테고리 (경로 분석):")
        categories = self.extract_categories(admin_endpoints + front_endpoints)

        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"  - {category}: {count}개")

        return {
            'complete_endpoints': complete_endpoints,
            'incomplete_endpoints': incomplete_endpoints,
            'method_counts': dict(method_counts),
            'categories': dict(categories)
        }

    def extract_categories(self, endpoints):
        """경로에서 카테고리 추출"""
        categories = defaultdict(int)

        for ep in endpoints:
            path = ep.get('path', '')

            # /api/v2/admin/{category} 형식에서 카테고리 추출
            match = re.search(r'/api/v2/(admin|front)/([^/?]+)', path)
            if match:
                category = match.group(2)
                categories[category] += 1

        return categories

    def categorize_endpoints(self):
        """엔드포인트를 카테고리별로 분류"""
        print("\n" + "="*60)
        print("📂 카테고리별 분류")
        print("="*60)

        admin_endpoints = self.admin_data['endpoints']
        front_endpoints = self.front_data['endpoints']

        # Admin API 분류
        admin_categorized = defaultdict(list)
        for ep in admin_endpoints:
            category = self.get_category(ep['path'], 'admin')
            admin_categorized[category].append(ep)

        # Front API 분류
        front_categorized = defaultdict(list)
        for ep in front_endpoints:
            category = self.get_category(ep['path'], 'front')
            front_categorized[category].append(ep)

        print(f"\n📋 Admin API 카테고리 ({len(admin_categorized)}개):")
        for category, eps in sorted(admin_categorized.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  - {category}: {len(eps)}개 엔드포인트")

        print(f"\n📋 Front API 카테고리 ({len(front_categorized)}개):")
        for category, eps in sorted(front_categorized.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  - {category}: {len(eps)}개 엔드포인트")

        return {
            'admin': dict(admin_categorized),
            'front': dict(front_categorized)
        }

    def get_category(self, path, api_type):
        """경로에서 카테고리 추출"""
        if api_type == 'admin':
            # Admin API: /api/v2/admin/{category}
            match = re.search(r'/api/v2/admin/([^/?]+)', path)
            if match:
                return match.group(1)
        else:
            # Front API: /api/v2/{category} (front 없음)
            match = re.search(r'/api/v2/([^/?]+)', path)
            if match:
                category = match.group(1)
                # Front API 주요 카테고리 매핑
                if category in ['products', 'productsdetail']:
                    return 'products'
                elif category == 'categories':
                    return 'categories'
                elif category in ['carts', 'mains']:
                    return 'personal'
                return category
        return 'other'

    def create_categorized_files(self, categorized_data):
        """카테고리별 파일 생성"""
        print("\n" + "="*60)
        print("📝 카테고리별 파일 생성")
        print("="*60)

        output_dir = Path("docs/cafe24/categories")
        output_dir.mkdir(exist_ok=True)

        # Admin API 카테고리별 파일
        admin_dir = output_dir / "admin"
        admin_dir.mkdir(exist_ok=True)

        for category, endpoints in categorized_data['admin'].items():
            file_path = admin_dir / f"{category}.json"

            data = {
                "category": category,
                "api_type": "admin",
                "endpoint_count": len(endpoints),
                "endpoints": endpoints
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"  ✓ {file_path} ({len(endpoints)}개 엔드포인트)")

        # Front API 카테고리별 파일
        front_dir = output_dir / "front"
        front_dir.mkdir(exist_ok=True)

        for category, endpoints in categorized_data['front'].items():
            file_path = front_dir / f"{category}.json"

            data = {
                "category": category,
                "api_type": "front",
                "endpoint_count": len(endpoints),
                "endpoints": endpoints
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"  ✓ {file_path} ({len(endpoints)}개 엔드포인트)")

    def create_index(self, categorized_data):
        """전체 인덱스 생성"""
        print("\n" + "="*60)
        print("🗺️  인덱스 파일 생성")
        print("="*60)

        index = {
            "title": "Cafe24 API Documentation Index",
            "description": "Complete reference for all Cafe24 Admin and Front APIs",
            "version": "2.0",
            "total_categories": len(categorized_data['admin']) + len(categorized_data['front']),
            "total_endpoints": sum(len(eps) for eps in categorized_data['admin'].values()) +
                              sum(len(eps) for eps in categorized_data['front'].values()),
            "admin_api": {},
            "front_api": {},
            "quick_reference": {}
        }

        # Admin API 인덱스
        for category, endpoints in sorted(categorized_data['admin'].items()):
            methods = defaultdict(list)
            for ep in endpoints:
                methods[ep['method']].append({
                    "path": ep['path'],
                    "summary": ep.get('summary', '')
                })

            index['admin_api'][category] = {
                "file": f"categories/admin/{category}.json",
                "endpoint_count": len(endpoints),
                "methods": dict(methods),
                "description": self.get_category_description(category)
            }

        # Front API 인덱스
        for category, endpoints in sorted(categorized_data['front'].items()):
            methods = defaultdict(list)
            for ep in endpoints:
                methods[ep['method']].append({
                    "path": ep['path'],
                    "summary": ep.get('summary', '')
                })

            index['front_api'][category] = {
                "file": f"categories/front/{category}.json",
                "endpoint_count": len(endpoints),
                "methods": dict(methods),
                "description": self.get_category_description(category)
            }

        # Quick Reference (주요 API만)
        index['quick_reference'] = self.create_quick_reference(categorized_data)

        # 저장
        index_file = "docs/cafe24/api-index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"  ✓ {index_file} 생성 완료")

        # README도 생성
        self.create_readme(index)

    def get_category_description(self, category):
        """카테고리 설명"""
        descriptions = {
            # Admin API
            'products': '상품 관리 (등록, 수정, 조회, 삭제)',
            'categories': '카테고리 관리',
            'orders': '주문 관리',
            'customers': '고객/회원 관리',
            'shipping': '배송 관리',
            'mileage': '적립금 관리',
            'coupons': '쿠폰 관리',
            'points': '포인트 관리',
            'boards': '게시판 관리',
            'articles': '게시글 관리',
            'reviews': '상품평 관리',
            'payments': '결제 관리',
            'store': '쇼핑몰 기본 정보',
            'application': '앱 설정',
            'oauth': 'OAuth 인증',
            'shops': '멀티쇼핑몰 관리',
            'variants': '상품 옵션/품목',
            'inventories': '재고 관리',
            'benefits': '혜택/프로모션',
            'salesreport': '매출 통계',
            # Front API
            'personal': '개인화 정보 (장바구니, 메인화면)',
            'other': '기타'
        }
        return descriptions.get(category, category)

    def create_quick_reference(self, categorized_data):
        """자주 쓰는 API 빠른 참조"""
        # 주요 카테고리만 선별
        important_categories = [
            'products', 'categories', 'orders', 'customers',
            'shipping', 'coupons', 'oauth', 'store'
        ]

        quick_ref = {}

        for category in important_categories:
            if category in categorized_data['admin']:
                endpoints = categorized_data['admin'][category]
                quick_ref[category] = {
                    "api_type": "admin",
                    "file": f"categories/admin/{category}.json",
                    "common_operations": self.extract_common_operations(endpoints)
                }

        return quick_ref

    def extract_common_operations(self, endpoints):
        """일반적인 CRUD 작업 추출"""
        operations = {}

        for ep in endpoints:
            method = ep['method']
            path = ep['path']
            summary = ep.get('summary', '')

            # 목록 조회
            if method == 'GET' and not re.search(r'/\d+', path) and not re.search(r'/\{', path):
                if 'list' not in operations:
                    operations['list'] = {"method": method, "path": path, "summary": summary}

            # 상세 조회
            elif method == 'GET' and (re.search(r'/\d+', path) or re.search(r'/\{[^}]+\}', path)):
                if 'get' not in operations:
                    operations['get'] = {"method": method, "path": path, "summary": summary}

            # 생성
            elif method == 'POST':
                if 'create' not in operations:
                    operations['create'] = {"method": method, "path": path, "summary": summary}

            # 수정
            elif method == 'PUT':
                if 'update' not in operations:
                    operations['update'] = {"method": method, "path": path, "summary": summary}

            # 삭제
            elif method == 'DELETE':
                if 'delete' not in operations:
                    operations['delete'] = {"method": method, "path": path, "summary": summary}

        return operations

    def create_readme(self, index):
        """README.md 생성"""
        readme_content = f"""# Cafe24 API Documentation

## 📊 개요

- **총 카테고리**: {index['total_categories']}개
- **총 엔드포인트**: {index['total_endpoints']}개
- **Admin API**: {len(index['admin_api'])}개 카테고리
- **Front API**: {len(index['front_api'])}개 카테고리

## 📂 파일 구조

```
docs/cafe24/
├── api-index.json              # 전체 API 인덱스 (이 문서)
├── cafe24-openapi.json         # OpenAPI 3.0 전체 스펙
├── specs/
│   ├── admin.json              # Admin API 전체
│   └── front.json              # Front API 전체
└── categories/
    ├── admin/                  # Admin API 카테고리별
    │   ├── products.json
    │   ├── orders.json
    │   ├── customers.json
    │   └── ...
    └── front/                  # Front API 카테고리별
        └── ...
```

## 🚀 사용법

### 1. 전체 API 참조

```bash
# OpenAPI 전체 스펙
cat docs/cafe24/cafe24-openapi.json

# Admin API 전체
cat docs/cafe24/specs/admin.json

# Front API 전체
cat docs/cafe24/specs/front.json
```

### 2. 카테고리별 참조

```bash
# 상품 API만
cat docs/cafe24/categories/admin/products.json

# 주문 API만
cat docs/cafe24/categories/admin/orders.json
```

### 3. Claude Code에서 사용

```
"docs/cafe24/categories/admin/products.json을 참고해서
 상품 등록 기능을 구현해줘"
```

## 📋 Admin API 카테고리

"""
        for category, info in sorted(index['admin_api'].items(), key=lambda x: x[1]['endpoint_count'], reverse=True):
            readme_content += f"### {category.capitalize()}\n"
            readme_content += f"- **설명**: {info['description']}\n"
            readme_content += f"- **엔드포인트**: {info['endpoint_count']}개\n"
            readme_content += f"- **파일**: `{info['file']}`\n"

            if info['methods']:
                readme_content += f"- **메서드**: {', '.join(info['methods'].keys())}\n"

            readme_content += "\n"

        readme_content += f"""
## 📋 Front API 카테고리

"""
        for category, info in sorted(index['front_api'].items(), key=lambda x: x[1]['endpoint_count'], reverse=True):
            readme_content += f"### {category.capitalize()}\n"
            readme_content += f"- **설명**: {info['description']}\n"
            readme_content += f"- **엔드포인트**: {info['endpoint_count']}개\n"
            readme_content += f"- **파일**: `{info['file']}`\n\n"

        readme_content += """
## 🔍 빠른 참조 (Quick Reference)

자주 사용하는 API:

"""
        for category, info in index['quick_reference'].items():
            readme_content += f"### {category.capitalize()}\n"
            readme_content += f"**파일**: `{info['file']}`\n\n"

            if 'common_operations' in info:
                readme_content += "| 작업 | 메서드 | 경로 |\n"
                readme_content += "|------|--------|------|\n"
                for op_name, op_info in info['common_operations'].items():
                    readme_content += f"| {op_name} | {op_info['method']} | {op_info['path']} |\n"
                readme_content += "\n"

        readme_content += """
## 💡 팁

1. **전체 검색**: `api-index.json`에서 필요한 API 찾기
2. **카테고리별 작업**: `categories/{api_type}/{category}.json` 사용
3. **OpenAPI 도구**: `cafe24-openapi.json`을 Swagger UI에서 열기

---

생성 날짜: Vision AI 스크래핑으로 자동 생성
"""

        readme_file = "docs/cafe24/README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        print(f"  ✓ {readme_file} 생성 완료")

def main():
    verifier = APIVerifier()

    print("\n" + "="*60)
    print("🔍 Cafe24 API 검증 및 구조화")
    print("="*60)

    # 1. 데이터 로드
    print("\n📂 데이터 로드 중...")
    verifier.load_data()
    print("  ✓ 로드 완료")

    # 2. 품질 검증
    verification_result = verifier.verify_data_quality()

    # 3. 카테고리별 분류
    categorized_data = verifier.categorize_endpoints()

    # 4. 카테고리별 파일 생성
    verifier.create_categorized_files(categorized_data)

    # 5. 인덱스 생성
    verifier.create_index(categorized_data)

    print("\n" + "="*60)
    print("✅ 모든 작업 완료!")
    print("="*60)
    print("\n📁 생성된 파일:")
    print("  - docs/cafe24/api-index.json (전체 인덱스)")
    print("  - docs/cafe24/README.md (사용 가이드)")
    print("  - docs/cafe24/categories/admin/*.json (Admin API 카테고리별)")
    print("  - docs/cafe24/categories/front/*.json (Front API 카테고리별)")

if __name__ == "__main__":
    main()
