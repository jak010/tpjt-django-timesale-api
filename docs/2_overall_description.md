# 2. 전체 문서 (Overall Description)

## 2.1 Product Perspective (제품 조망)

타임세일 API는 전자상거래 플랫폼의 핵심 마케팅 도구로서, 시간 제한이 있는 할인 상품 판매를 효율적으로 관리하기 위한 독립적인 백엔드 서비스입니다.
본 시스템은 Django REST Framework를 기반으로 구축되어, RESTful API 인터페이스를 통해 타임세일 관련 모든 비즈니스 로직을 처리합니다.

### 2.1.1 주요 도메인 모델

#### 2.1.1.1 Product (상품)

상품 정보를 나타내는 도메인 모델입니다. 상품 ID, 이름, 가격, 설명 등의 속성을 가집니다.

- 타임세일 대상이 되는 기본 상품 정보
- 상품명, 원가격, 상품 설명 등의 기본 속성 관리

| 속성            | 설명               |
|---------------|------------------|
| `product_id`  | 상품의 고유 식별자입니다.   |
| `name`        | 상품의 이름입니다.       |
| `price`       | 상품의 가격입니다.       |
| `description` | 상품에 대한 상세 설명입니다. |

#### 2.1.1.2 TimeSale (타임세일)

- 타임 세일 정보를 나타내는 도메인 모델입니다. 상품, 수량, 할인 가격, 시작/종료 시간, 상태 등의 속성을 가집니다.
    - 특정 상품에 대한 시간 한정 할인 이벤트
    - 할인 가격, 할인 수량, 세일 기간 등의 세일 관련 정보
    - ACTIVE/INACTIVE 상태를 통한 세일 활성화 제어

| 속성                   | 설명                                   |
|----------------------|--------------------------------------|
| `timesale_id`        | 타임 세일의 고유 식별자입니다.                    |
| `product`            | 타임 세일이 적용되는 상품입니다.                   |
| `quantity`           | 타임 세일로 판매되는 총 수량입니다.                 |
| `remaining_quantity` | 타임 세일로 판매 가능한 남은 수량입니다.              |
| `discount_price`     | 타임 세일이 적용된 할인 가격입니다.                 |
| `start_at`           | 타임 세일 시작 시간입니다.                      |
| `end_at`             | 타임 세일 종료 시간입니다.                      |
| `status`             | 타임 세일의 상태를 나타냅니다. (ACTIVE, INACTIVE) |

#### 2.1.1.3 TimeSaleOrder (타임세일 주문)

- 타임 세일 주문 정보를 나타내는 도메인 모델입니다.
    - 사용자 ID, 타임 세일, 수량, 할인 가격, 주문 상태 등의 속성을 가집니다.

| 속성                  | 설명                                             |
|---------------------|------------------------------------------------|
| `timesale_order_id` | 타임 세일 주문의 고유 식별자입니다.                           |
| `user_id`           | 주문한 사용자의 ID입니다.                                |
| `time_sale`         | 주문과 관련된 타임 세일입니다.                              |
| `quantity`          | 주문한 수량입니다.                                     |
| `discount_price`    | 주문에 적용된 할인 가격입니다.                              |
| `status`            | 주문의 현재 상태를 나타냅니다. (PENDING, COMPLETED, FAILED) |

## 2.2 Overall System Configuration (전체 시스템 구성)

## 2.3 Overall Operation (전체 동작방식)

## 2.4 Product Functions (제품 주요 기능)

| 분류          | 기능명           | API 함수명                 | 주요 내용                                                                                                                  | 테스트 케이스 목록                                                                                                                                                                                                                                                                      |
|-------------|---------------|-------------------------|------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **상품 관리**   | 상품 생성         | `create_product`        | - 새로운 상품을 시스템에 등록<br>- 상품명, 가격, 상품 설명 정보 관리                                                                            | - test_create_product_success<br>- test_create_product_missing_name<br>- test_create_product_missing_price<br>- test_create_product_missing_description<br>- test_create_product_invalid_price_type<br>- test_create_product_empty_name<br>- test_create_product_negative_price |
|             | 상품 조회         | `get_product`           | - 특정 상품의 상세 정보 조회                                                                                                      | - test_get_product_existing_id<br>- test_get_product_non_existing_id                                                                                                                                                                                                            |
|             | 상품 목록         | `get_all_products`      | - 전체 상품 목록 조회                                                                                                          | - test_get_all_products_with_data<br>- test_get_all_products_empty<br>- test_get_all_products_large_dataset                                                                                                                                                                     |
| **타임세일 관리** | 타임세일 생성       | `create_timesale`       | - 새로운 타임세일 이벤트 생성<br>- 상품 ID, 할인 수량, 할인 가격 설정<br>- 세일 시작/종료 시간 설정                                                      | - test_create_timesale_success<br>- test_create_timesale_fail_due_to_invalid_time<br>- test_create_timesale_with_not_exit_product                                                                                                                                               |
|             | 타임세일 조회       | `get_timesale`          | - 특정 타임세일 정보 조회                                                                                                        | - test_get_timesale_success<br>- test_get_timesale_not_found                                                                                                                                                                                                                    |
|             | 진행 중인 타임세일 목록 | `get_ongoing_timesales` | - 현재 활성화된 타임세일 페이지네이션 조회<br>- 시작 시간 ≤ 현재 시간 ≤ 종료 시간 조건 필터링<br>- 상태가 ACTIVE인 타임세일만 조회<br>- 페이지 기반 목록 조회 지원              | - test_get_ongoing_timesales_success<br>- test_get_ongoing_timesales_empty                                                                                                                                                                                                      |
| **구매 처리**   | 타임세일 구매       | `purchase_time_sale`    | - 타임세일 상품 구매 처리<br>- 비관적 락(Pessimistic Lock)을 통한 동시성 제어<br>- 실시간 재고 차감 처리<br>- 주문 객체 생성 및 상태 관리<br>- 트랜잭션 기반 안전한 구매 처리 | - test_purchase_timesale_success<br>- test_purchase_timesale_out_of_stock                                                                                                                                                                                                       |

## 2.5 User Classes and Characteristics (사용자 계층과 특징)

## 2.6 Assumptions and Dependencies (가정과 종속 관계)

## 2.7 Apportioning of Requirements (단계별 요구사항)

## 2.8 Backward compatibility (하위 호환성)
