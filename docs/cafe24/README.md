# Cafe24 API Documentation

## 📊 개요

- **총 카테고리**: 93개
- **총 엔드포인트**: 535개
- **Admin API**: 90개 카테고리
- **Front API**: 3개 카테고리

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

### Products
- **설명**: 상품 관리 (등록, 수정, 조회, 삭제)
- **엔드포인트**: 73개
- **파일**: `categories/admin/products.json`
- **메서드**: GET, PUT, POST, DELETE

### Orders
- **설명**: 주문 관리
- **엔드포인트**: 70개
- **파일**: `categories/admin/orders.json`
- **메서드**: GET, PUT, DELETE, POST

### Customers
- **설명**: 고객/회원 관리
- **엔드포인트**: 24개
- **파일**: `categories/admin/customers.json`
- **메서드**: GET, PUT, DELETE, POST

### Categories
- **설명**: 카테고리 관리
- **엔드포인트**: 20개
- **파일**: `categories/admin/categories.json`
- **메서드**: GET, PUT, POST, DELETE

### Suppliers
- **설명**: suppliers
- **엔드포인트**: 17개
- **파일**: `categories/admin/suppliers.json`
- **메서드**: GET, POST, PUT, DELETE

### Boards
- **설명**: 게시판 관리
- **엔드포인트**: 15개
- **파일**: `categories/admin/boards.json`
- **메서드**: GET, PUT, POST, DELETE

### Mains
- **설명**: mains
- **엔드포인트**: 14개
- **파일**: `categories/admin/mains.json`
- **메서드**: GET, PUT, POST, DELETE

### Translations
- **설명**: translations
- **엔드포인트**: 9개
- **파일**: `categories/admin/translations.json`
- **메서드**: GET, PUT

### Benefits
- **설명**: 혜택/프로모션
- **엔드포인트**: 8개
- **파일**: `categories/admin/benefits.json`
- **메서드**: GET, PUT, POST, DELETE

### Coupons
- **설명**: 쿠폰 관리
- **엔드포인트**: 8개
- **파일**: `categories/admin/coupons.json`
- **메서드**: GET, PUT, POST

### Points
- **설명**: 포인트 관리
- **엔드포인트**: 8개
- **파일**: `categories/admin/points.json`
- **메서드**: GET, PUT, POST, DELETE

### Subscription
- **설명**: subscription
- **엔드포인트**: 8개
- **파일**: `categories/admin/subscription.json`
- **메서드**: GET, POST, PUT, DELETE

### Paymentgateway
- **설명**: paymentgateway
- **엔드포인트**: 7개
- **파일**: `categories/admin/paymentgateway.json`
- **메서드**: POST, PUT, DELETE, GET

### Socials
- **설명**: socials
- **엔드포인트**: 7개
- **파일**: `categories/admin/socials.json`
- **메서드**: GET, PUT

### Themes
- **설명**: themes
- **엔드포인트**: 7개
- **파일**: `categories/admin/themes.json`
- **메서드**: GET, POST, PUT, DELETE

### Financials
- **설명**: financials
- **엔드포인트**: 6개
- **파일**: `categories/admin/financials.json`
- **메서드**: GET

### Orderform
- **설명**: orderform
- **엔드포인트**: 6개
- **파일**: `categories/admin/orderform.json`
- **메서드**: GET, PUT, POST, DELETE

### Privacy
- **설명**: privacy
- **엔드포인트**: 6개
- **파일**: `categories/admin/privacy.json`
- **메서드**: GET, PUT

### Scripttags
- **설명**: scripttags
- **엔드포인트**: 6개
- **파일**: `categories/admin/scripttags.json`
- **메서드**: GET, POST, PUT, DELETE

### Sms
- **설명**: sms
- **엔드포인트**: 6개
- **파일**: `categories/admin/sms.json`
- **메서드**: GET, PUT, POST

### Brands
- **설명**: brands
- **엔드포인트**: 5개
- **파일**: `categories/admin/brands.json`
- **메서드**: GET, POST, PUT, DELETE

### Bundleproducts
- **설명**: bundleproducts
- **엔드포인트**: 5개
- **파일**: `categories/admin/bundleproducts.json`
- **메서드**: GET, POST, PUT, DELETE

### Carriers
- **설명**: carriers
- **엔드포인트**: 5개
- **파일**: `categories/admin/carriers.json`
- **메서드**: GET, POST, PUT, DELETE

### Customergroups
- **설명**: customergroups
- **엔드포인트**: 5개
- **파일**: `categories/admin/customergroups.json`
- **메서드**: GET, POST

### Discountcodes
- **설명**: discountcodes
- **엔드포인트**: 5개
- **파일**: `categories/admin/discountcodes.json`
- **메서드**: GET, POST, PUT, DELETE

### Manufacturers
- **설명**: manufacturers
- **엔드포인트**: 5개
- **파일**: `categories/admin/manufacturers.json`
- **메서드**: GET, POST, PUT

### Recipientgroups
- **설명**: recipientgroups
- **엔드포인트**: 5개
- **파일**: `categories/admin/recipientgroups.json`
- **메서드**: GET, POST, PUT, DELETE

### Serialcoupons
- **설명**: serialcoupons
- **엔드포인트**: 5개
- **파일**: `categories/admin/serialcoupons.json`
- **메서드**: GET, POST, DELETE

### Shippingorigins
- **설명**: shippingorigins
- **엔드포인트**: 5개
- **파일**: `categories/admin/shippingorigins.json`
- **메서드**: GET, POST, PUT, DELETE

### Appstore
- **설명**: appstore
- **엔드포인트**: 4개
- **파일**: `categories/admin/appstore.json`
- **메서드**: GET, POST

### Autodisplay
- **설명**: autodisplay
- **엔드포인트**: 4개
- **파일**: `categories/admin/autodisplay.json`
- **메서드**: GET, POST, PUT, DELETE

### Cashreceipt
- **설명**: cashreceipt
- **엔드포인트**: 4개
- **파일**: `categories/admin/cashreceipt.json`
- **메서드**: GET, POST, PUT

### Commonevents
- **설명**: commonevents
- **엔드포인트**: 4개
- **파일**: `categories/admin/commonevents.json`
- **메서드**: GET, POST, PUT, DELETE

### Customersprivacy
- **설명**: customersprivacy
- **엔드포인트**: 4개
- **파일**: `categories/admin/customersprivacy.json`
- **메서드**: GET, PUT

### Other
- **설명**: 기타
- **엔드포인트**: 4개
- **파일**: `categories/admin/other.json`
- **메서드**: GET, POST

### Redirects
- **설명**: redirects
- **엔드포인트**: 4개
- **파일**: `categories/admin/redirects.json`
- **메서드**: GET, POST, PUT, DELETE

### Shipping
- **설명**: 배송 관리
- **엔드포인트**: 4개
- **파일**: `categories/admin/shipping.json`
- **메서드**: GET, PUT

### Urgentinquiry
- **설명**: urgentinquiry
- **엔드포인트**: 4개
- **파일**: `categories/admin/urgentinquiry.json`
- **메서드**: GET, POST, PUT

### Automessages
- **설명**: automessages
- **엔드포인트**: 3개
- **파일**: `categories/admin/automessages.json`
- **메서드**: GET, PUT

### Cancellation
- **설명**: cancellation
- **엔드포인트**: 3개
- **파일**: `categories/admin/cancellation.json`
- **메서드**: GET, POST, PUT

### Carts
- **설명**: carts
- **엔드포인트**: 3개
- **파일**: `categories/admin/carts.json`
- **메서드**: GET, PUT

### Commenttemplates
- **설명**: commenttemplates
- **엔드포인트**: 3개
- **파일**: `categories/admin/commenttemplates.json`
- **메서드**: GET, POST

### Customerevents
- **설명**: customerevents
- **엔드포인트**: 3개
- **파일**: `categories/admin/customerevents.json`
- **메서드**: GET, POST, PUT

### Exchange
- **설명**: exchange
- **엔드포인트**: 3개
- **파일**: `categories/admin/exchange.json`
- **메서드**: GET, POST, PUT

### Kakaoalimtalk
- **설명**: kakaoalimtalk
- **엔드포인트**: 3개
- **파일**: `categories/admin/kakaoalimtalk.json`
- **메서드**: GET, PUT

### Naverpay
- **설명**: naverpay
- **엔드포인트**: 3개
- **파일**: `categories/admin/naverpay.json`
- **메서드**: GET, POST, PUT

### Paymentmethods
- **설명**: paymentmethods
- **엔드포인트**: 3개
- **파일**: `categories/admin/paymentmethods.json`
- **메서드**: GET, PUT

### Recipes
- **설명**: recipes
- **엔드포인트**: 3개
- **파일**: `categories/admin/recipes.json`
- **메서드**: GET, POST, DELETE

### Reports
- **설명**: reports
- **엔드포인트**: 3개
- **파일**: `categories/admin/reports.json`
- **메서드**: GET

### Return
- **설명**: return
- **엔드포인트**: 3개
- **파일**: `categories/admin/return.json`
- **메서드**: GET, POST, PUT

### Webhooks
- **설명**: webhooks
- **엔드포인트**: 3개
- **파일**: `categories/admin/webhooks.json`
- **메서드**: GET, PUT

### Activitylogs
- **설명**: activitylogs
- **엔드포인트**: 2개
- **파일**: `categories/admin/activitylogs.json`
- **메서드**: GET

### Apps
- **설명**: apps
- **엔드포인트**: 2개
- **파일**: `categories/admin/apps.json`
- **메서드**: GET, PUT

### Automails
- **설명**: automails
- **엔드포인트**: 2개
- **파일**: `categories/admin/automails.json`
- **메서드**: GET, PUT

### Cancellationrequests
- **설명**: cancellationrequests
- **엔드포인트**: 2개
- **파일**: `categories/admin/cancellationrequests.json`
- **메서드**: POST, PUT

### Classifications
- **설명**: classifications
- **엔드포인트**: 2개
- **파일**: `categories/admin/classifications.json`
- **메서드**: GET

### Credits
- **설명**: credits
- **엔드포인트**: 2개
- **파일**: `categories/admin/credits.json`
- **메서드**: GET

### Currency
- **설명**: currency
- **엔드포인트**: 2개
- **파일**: `categories/admin/currency.json`
- **메서드**: GET, PUT

### Dormantaccount
- **설명**: dormantaccount
- **엔드포인트**: 2개
- **파일**: `categories/admin/dormantaccount.json`
- **메서드**: GET, PUT

### Exchangerequests
- **설명**: exchangerequests
- **엔드포인트**: 2개
- **파일**: `categories/admin/exchangerequests.json`
- **메서드**: POST, PUT

### Images
- **설명**: images
- **엔드포인트**: 2개
- **파일**: `categories/admin/images.json`
- **메서드**: GET, PUT

### Information
- **설명**: information
- **엔드포인트**: 2개
- **파일**: `categories/admin/information.json`
- **메서드**: GET, PUT

### Kakaopay
- **설명**: kakaopay
- **엔드포인트**: 2개
- **파일**: `categories/admin/kakaopay.json`
- **메서드**: GET, PUT

### Labels
- **설명**: labels
- **엔드포인트**: 2개
- **파일**: `categories/admin/labels.json`
- **메서드**: GET, POST

### Mobile
- **설명**: mobile
- **엔드포인트**: 2개
- **파일**: `categories/admin/mobile.json`
- **메서드**: GET, PUT

### Payment
- **설명**: payment
- **엔드포인트**: 2개
- **파일**: `categories/admin/payment.json`
- **메서드**: GET, PUT

### Policy
- **설명**: policy
- **엔드포인트**: 2개
- **파일**: `categories/admin/policy.json`
- **메서드**: GET, PUT

### Refunds
- **설명**: refunds
- **엔드포인트**: 2개
- **파일**: `categories/admin/refunds.json`
- **메서드**: GET

### Regionalsurcharges
- **설명**: regionalsurcharges
- **엔드포인트**: 2개
- **파일**: `categories/admin/regionalsurcharges.json`
- **메서드**: GET, PUT

### Restocknotification
- **설명**: restocknotification
- **엔드포인트**: 2개
- **파일**: `categories/admin/restocknotification.json`
- **메서드**: GET, PUT

### Returnrequests
- **설명**: returnrequests
- **엔드포인트**: 2개
- **파일**: `categories/admin/returnrequests.json`
- **메서드**: POST, PUT

### Seo
- **설명**: seo
- **엔드포인트**: 2개
- **파일**: `categories/admin/seo.json`
- **메서드**: GET, PUT

### Shipments
- **설명**: shipments
- **엔드포인트**: 2개
- **파일**: `categories/admin/shipments.json`
- **메서드**: POST, PUT

### Shops
- **설명**: 멀티쇼핑몰 관리
- **엔드포인트**: 2개
- **파일**: `categories/admin/shops.json`
- **메서드**: GET

### Store
- **설명**: 쇼핑몰 기본 정보
- **엔드포인트**: 2개
- **파일**: `categories/admin/store.json`
- **메서드**: GET

### Trends
- **설명**: trends
- **엔드포인트**: 2개
- **파일**: `categories/admin/trends.json`
- **메서드**: GET

### Users
- **설명**: users
- **엔드포인트**: 2개
- **파일**: `categories/admin/users.json`
- **메서드**: GET

### Collectrequests
- **설명**: collectrequests
- **엔드포인트**: 1개
- **파일**: `categories/admin/collectrequests.json`
- **메서드**: PUT

### Control
- **설명**: control
- **엔드포인트**: 1개
- **파일**: `categories/admin/control.json`
- **메서드**: PUT

### Dashboard
- **설명**: dashboard
- **엔드포인트**: 1개
- **파일**: `categories/admin/dashboard.json`
- **메서드**: GET

### Databridge
- **설명**: databridge
- **엔드포인트**: 1개
- **파일**: `categories/admin/databridge.json`
- **메서드**: GET

### Fulfillments
- **설명**: fulfillments
- **엔드포인트**: 1개
- **파일**: `categories/admin/fulfillments.json`
- **메서드**: POST

### Icons
- **설명**: icons
- **엔드포인트**: 1개
- **파일**: `categories/admin/icons.json`
- **메서드**: GET

### Menus
- **설명**: menus
- **엔드포인트**: 1개
- **파일**: `categories/admin/menus.json`
- **메서드**: GET

### Origin
- **설명**: origin
- **엔드포인트**: 1개
- **파일**: `categories/admin/origin.json`
- **메서드**: GET

### Payments
- **설명**: 결제 관리
- **엔드포인트**: 1개
- **파일**: `categories/admin/payments.json`
- **메서드**: PUT

### Reservations
- **설명**: reservations
- **엔드포인트**: 1개
- **파일**: `categories/admin/reservations.json`
- **메서드**: GET

### Shippingmanager
- **설명**: shippingmanager
- **엔드포인트**: 1개
- **파일**: `categories/admin/shippingmanager.json`
- **메서드**: GET

### Taxmanager
- **설명**: taxmanager
- **엔드포인트**: 1개
- **파일**: `categories/admin/taxmanager.json`
- **메서드**: GET

### Unpaidorders
- **설명**: unpaidorders
- **엔드포인트**: 1개
- **파일**: `categories/admin/unpaidorders.json`
- **메서드**: GET


## 📋 Front API 카테고리

### Products
- **설명**: 상품 관리 (등록, 수정, 조회, 삭제)
- **엔드포인트**: 18개
- **파일**: `categories/front/products.json`

### Categories
- **설명**: 카테고리 관리
- **엔드포인트**: 5개
- **파일**: `categories/front/categories.json`

### Personal
- **설명**: 개인화 정보 (장바구니, 메인화면)
- **엔드포인트**: 2개
- **파일**: `categories/front/personal.json`


## 🔍 빠른 참조 (Quick Reference)

자주 사용하는 API:

### Products
**파일**: `categories/admin/products.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| list | GET | /api/v2/admin/products |
| get | GET | /api/v2/admin/products/128 |
| update | PUT | /api/v2/admin/products/properties/setting |
| create | POST | /api/v2/admin/products |
| delete | DELETE | /api/v2/admin/products/{product_no} |

### Categories
**파일**: `categories/admin/categories.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| list | GET | /api/v2/admin/categories/properties/setting |
| update | PUT | /api/v2/admin/categories/properties/setting |
| get | GET | /api/v2/admin/categories/{category_no}/products |
| create | POST | /api/v2/admin/categories/{category_no}/products |
| delete | DELETE | /api/v2/admin/categories/{category_no}/products/{product_no} |

### Orders
**파일**: `categories/admin/orders.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| list | GET | /api/v2/admin/orders/setting |
| update | PUT | /api/v2/admin/orders/setting |
| get | GET | /api/v2/admin/orders/{order_id} |
| delete | DELETE | /api/v2/admin/orders/{order_id}/autocalculation |
| create | POST | /api/v2/admin/orders/{order_id}/cancellation |

### Customers
**파일**: `categories/admin/customers.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| list | GET | /api/v2/admin/customers/setting |
| update | PUT | /api/v2/admin/customers/setting |
| delete | DELETE | /api/v2/admin/customers/{member_id} |
| get | GET | /api/v2/admin/customers/{member_id}/autoupdate |
| create | POST | /api/v2/admin/customers/{member_id}/memos |

### Shipping
**파일**: `categories/admin/shipping.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| get | GET | /api/v2/admin/shipping/suppliers/{supplier_id} |
| update | PUT | /api/v2/admin/shipping/suppliers/{supplier_id} |
| list | GET | /api/v2/admin/shipping |

### Coupons
**파일**: `categories/admin/coupons.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| list | GET | /api/v2/admin/coupons/setting |
| update | PUT | /api/v2/admin/coupons/setting |
| create | POST | /api/v2/admin/coupons |
| get | GET | /api/v2/admin/coupons/{coupon_no}/issues |

### Store
**파일**: `categories/admin/store.json`

| 작업 | 메서드 | 경로 |
|------|--------|------|
| list | GET | /api/v2/admin/store |


## 💡 팁

1. **전체 검색**: `api-index.json`에서 필요한 API 찾기
2. **카테고리별 작업**: `categories/{api_type}/{category}.json` 사용
3. **OpenAPI 도구**: `cafe24-openapi.json`을 Swagger UI에서 열기

---

생성 날짜: Vision AI 스크래핑으로 자동 생성
