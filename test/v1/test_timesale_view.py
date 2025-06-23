from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.dto.timsale_dto import TimeSaleCreateRequestDto, TimeSaleDetailResponseDto, TimeSaleOngoingResponseDto
from apps.models.enums.time_sale_status import TimeSaleStatus
from apps.models.product import Product
from apps.models.timesale import TimeSale


@pytest.mark.django_db
class TestTimeSaleView(APITestCase):

    def test_post_timesale_success(self):
        """ 타임세일 생성 성공 테스트 """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
        )
        product.save()

        url = reverse('timesales')  # router.py에 정의된 timesale-list URL 사용
        data = {
            "user_id": 1,
            "product_id": product.product_id,
            "quantity": 10,
            "discount_price": 10000,
            "start_at": "2025-01-01T00:00:00Z",
            "end_at": "2025-01-01T01:00:00Z"
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_post_timesale_invalid_data_failure(self):
        """ 타임세일 생성 실패 테스트 (유효하지 않은 데이터) """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
        )
        product.save()

        url = reverse('timesales')
        # TimeSaleCreateRequestDto를 사용하여 유효하지 않은 데이터 생성
        data = {
            "user_id": 1,
            "product_id": product.product_id,
            "quantity": 10,
            "discount_price": 10000,
            "start_at": "invalid-date",  # 유효하지 않은 날짜 형식
            "end_at": "2025-01-01T01:00:00Z"
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "start_at" in response.data


@pytest.mark.django_db
class TestTimeSaleDetailView(APITestCase):
    def test_get_timesale_detail_success(self):
        """ 타임세일 상세 조회 성공 테스트 """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
        )
        product.save()

        # 테스트용 TimeSale 생성
        timesale = TimeSale.init_entity(
            product=product,
            discount_price=10000,
            start_at=datetime.now(),
            end_at=datetime.now(),
            quantity=10,
            status=TimeSale.Status.ACTIVE
        )
        timesale.save()

        timesale_id = timesale.timesale_id
        url = reverse('timesales-detail', args=[timesale_id])  # router.py에 정의된 timesale-detail URL 사용

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_timesale_detail_not_found_failure(self):
        """ 타임세일 상세 조회 실패 테스트 (타임세일 없음) """
        timesale_id = 999  # 존재하지 않는 타임세일 ID
        url = reverse('timesales-detail', args=[timesale_id])

        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTimeSaleOngoingView(APITestCase):
    def test_get_ongoing_timesales_success(self):
        """ 진행중인 타임세일 조회 성공 테스트 """
        # 테스트용 Product 생성
        product1 = Product.init_entity(
            name="Test Product 1",
            description="This is test product 1.",
            price=20000,
        )
        product1.save()

        product2 = Product.init_entity(
            name="Test Product 2",
            description="This is test product 2.",
            price=30000,
        )
        product2.save()

        # 테스트용 TimeSale 생성
        timesale1 = TimeSale.init_entity(
            product=product1,
            discount_price=10000,
            start_at=datetime.now(),
            end_at=datetime.now(),
            quantity=10,
            status=TimeSale.Status.ACTIVE
        )
        timesale1.save()

        timesale2 = TimeSale.init_entity(
            product=product2,
            discount_price=10000,
            start_at=datetime.now(),
            end_at=datetime.now(),
            quantity=10,
            status=TimeSale.Status.ACTIVE
        )
        timesale2.save()

        url = reverse('timesales-ongoing')  # router.py에 정의된 timesale-ongoing URL 사용

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_ongoing_timesales_no_results(self, ):
        """ 진행중인 타임세일 조회 실패 테스트 (결과 없음) """
        url = reverse('timesales-ongoing')

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


@pytest.mark.django_db
class TestTimeSaleOrderView(APITestCase):
    def test_post_timesale_purchase_success(self):
        """ 타임세일 구매 성공 테스트 """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000
        )
        product.save()

        # 테스트용 TimeSale 생성
        timesale = TimeSale.init_entity(
            product=product,
            discount_price=10000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            quantity=10,
            status=TimeSale.Status.ACTIVE
        )
        timesale.save()

        url = reverse('timesales-order', args=[timesale.timesale_id])  # router.py에 정의된 timesale-purchase URL 사용
        data = {
            "user_id": 1,
            "quantity": 1
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_post_timesale_purchase_invalid_data_failure(self):
        """ 타임세일 구매 실패 테스트 (유효하지 않은 데이터) """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000
        )
        product.save()

        # 테스트용 TimeSale 생성
        timesale = TimeSale.init_entity(
            product=product,
            discount_price=10000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            quantity=10,
            status=TimeSale.Status.ACTIVE
        )

        timesale.save()

        url = reverse('timesales-order', args=[timesale.timesale_id])  # router.py에 정의된 timesale-purchase URL 사용

        data = {
            "user_id": "invalid",  # 유효하지 않은 user_id
            "quantity": 1
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_timesale_purchase_service_error_failure(self):
        """ 타임세일 구매 실패 테스트 (서비스 에러) """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
        )
        product.save()
        # 테스트용 TimeSale 생성
        timesale = TimeSale.init_entity(
            product=product,
            discount_price=10000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            quantity=10,
            status=TimeSale.Status.ACTIVE
        )
        timesale.save()

        url = reverse('timesales-order', args=[timesale.timesale_id])  # router.py에 정의된 timesale-purchase URL 사용
        data = {
            "user_id": 1,
            "quantity": 22
        }

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
