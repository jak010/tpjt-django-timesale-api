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
            price=20000
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
    def test_get_timesale_detail_success(self, mock_timesale_service):
        """ 타임세일 상세 조회 성공 테스트 """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
        )
        product.save()
        # 테스트용 TimeSale 생성
        timesale = TimeSale.objects.create(
            product=product,
            sale_price=10000,
            start_time="2025-01-01T00:00:00Z",
            end_time="2025-01-01T01:00:00Z",
            quantity=10,
            status=TimeSaleStatus.ONGOING.value
        )
        timesale_id = timesale.id
        url = reverse('timesale-detail', args=[timesale_id])  # router.py에 정의된 timesale-detail URL 사용

        mock_timesale = MagicMock(spec=TimeSale)
        mock_timesale.id = timesale_id
        mock_timesale.product_id = product.id
        mock_timesale.sale_price = 10000
        mock_timesale.start_time = "2025-01-01T00:00:00Z"
        mock_timesale.end_time = "2025-01-01T01:00:00Z"
        mock_timesale.quantity = 10
        mock_timesale.status = TimeSaleStatus.ONGOING.value

        mock_timesale_service.get_timesale.return_value = mock_timesale

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == TimeSaleDetailResponseDto(mock_timesale).data
        mock_timesale_service.get_timesale.assert_called_once_with(timesale_id)

    def test_get_timesale_detail_not_found_failure(self, mock_timesale_service):
        """ 타임세일 상세 조회 실패 테스트 (타임세일 없음) """
        timesale_id = 999  # 존재하지 않는 타임세일 ID
        url = reverse('timesale-detail', args=[timesale_id])

        mock_timesale_service.get_timesale.return_value = None  # 타임세일이 없음을 시뮬레이션

        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_timesale_service.get_timesale.assert_called_once_with(timesale_id)


@pytest.mark.django_db
class TestTimeSaleOngoingView(APITestCase):
    def test_get_ongoing_timesales_success(self, mock_timesale_service):
        """ 진행중인 타임세일 조회 성공 테스트 """
        # 테스트용 Product 생성
        product1 = Product.init_entity(
            name="Test Product 1",
            description="This is test product 1.",
            price=20000,
            stock=100
        )
        product1.save()
        product2 = Product.init_entity(
            name="Test Product 2",
            description="This is test product 2.",
            price=30000,
            stock=150
        )
        product2.save()

        # 테스트용 TimeSale 생성
        timesale1 = TimeSale.objects.create(
            product=product1,
            sale_price=10000,
            start_time="2025-01-01T00:00:00Z",
            end_time="2025-01-01T01:00:00Z",
            quantity=10,
            status=TimeSaleStatus.ONGOING.value
        )
        timesale2 = TimeSale.objects.create(
            product=product2,
            sale_price=20000,
            start_time="2025-01-02T00:00:00Z",
            end_time="2025-01-02T01:00:00Z",
            quantity=20,
            status=TimeSaleStatus.ONGOING.value
        )

        url = reverse('timesale-ongoing')  # router.py에 정의된 timesale-ongoing URL 사용

        mock_timesale1 = MagicMock(spec=TimeSale)
        mock_timesale1.id = timesale1.id
        mock_timesale1.product_id = product1.id
        mock_timesale1.sale_price = 10000
        mock_timesale1.start_time = "2025-01-01T00:00:00Z"
        mock_timesale1.end_time = "2025-01-01T01:00:00Z"
        mock_timesale1.quantity = 10
        mock_timesale1.status = TimeSaleStatus.ONGOING.value

        mock_timesale2 = MagicMock(spec=TimeSale)
        mock_timesale2.id = timesale2.id
        mock_timesale2.product_id = product2.id
        mock_timesale2.sale_price = 20000
        mock_timesale2.start_time = "2025-01-02T00:00:00Z"
        mock_timesale2.end_time = "2025-01-02T01:00:00Z"
        mock_timesale2.quantity = 20
        mock_timesale2.status = TimeSaleStatus.ONGOING.value

        mock_timesales = [mock_timesale1, mock_timesale2]
        mock_timesale_service.get_ongoing_timesales.return_value = mock_timesales

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == TimeSaleOngoingResponseDto(mock_timesales, many=True).data
        mock_timesale_service.get_ongoing_timesales.assert_called_once_with(page=1, size=10)

    def test_get_ongoing_timesales_no_results(self, mock_timesale_service):
        """ 진행중인 타임세일 조회 실패 테스트 (결과 없음) """
        url = reverse('timesale-ongoing')

        mock_timesale_service.get_ongoing_timesales.return_value = []  # 결과가 없음을 시뮬레이션

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []
        mock_timesale_service.get_ongoing_timesales.assert_called_once_with(page=1, size=10)


@pytest.mark.django_db
class TestTimeSaleOrderView(APITestCase):
    def test_post_timesale_purchase_success(self, mock_timesale_service):
        """ 타임세일 구매 성공 테스트 """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
            stock=100
        )
        product.save()
        # 테스트용 TimeSale 생성
        timesale = TimeSale.objects.create(
            product=product,
            sale_price=10000,
            start_time="2025-01-01T00:00:00Z",
            end_time="2025-01-01T01:00:00Z",
            quantity=10,
            status=TimeSaleStatus.ONGOING.value
        )
        timesale_id = timesale.id
        url = reverse('timesale-purchase', args=[timesale_id])  # router.py에 정의된 timesale-purchase URL 사용
        data = {
            "user_id": 1,
            "quantity": 1
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        mock_timesale_service.purchase_time_sale.assert_called_once_with(timesale_id, data)

    def test_post_timesale_purchase_invalid_data_failure(self, mock_timesale_service):
        """ 타임세일 구매 실패 테스트 (유효하지 않은 데이터) """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
            stock=100
        )
        product.save()
        # 테스트용 TimeSale 생성
        timesale = TimeSale.objects.create(
            product=product,
            sale_price=10000,
            start_time="2025-01-01T00:00:00Z",
            end_time="2025-01-01T01:00:00Z",
            quantity=10,
            status=TimeSaleStatus.ONGOING.value
        )
        timesale_id = timesale.id
        url = reverse('timesale-purchase', args=[timesale_id])
        data = {
            "user_id": "invalid",  # 유효하지 않은 user_id
            "quantity": 1
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "user_id" in response.data
        mock_timesale_service.purchase_time_sale.assert_not_called()

    def test_post_timesale_purchase_service_error_failure(self, mock_timesale_service):
        """ 타임세일 구매 실패 테스트 (서비스 에러) """
        # 테스트용 Product 생성
        product = Product.init_entity(
            name="Test Product",
            description="This is a test product.",
            price=20000,
            stock=100
        )
        product.save()
        # 테스트용 TimeSale 생성
        timesale = TimeSale.objects.create(
            product=product,
            sale_price=10000,
            start_time="2025-01-01T00:00:00Z",
            end_time="2025-01-01T01:00:00Z",
            quantity=10,
            status=TimeSaleStatus.ONGOING.value
        )
        timesale_id = timesale.id
        url = reverse('timesale-purchase', args=[timesale_id])
        data = {
            "user_id": 1,
            "quantity": 1
        }
        mock_timesale_service.purchase_time_sale.side_effect = Exception("Service Error")

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Service Error" in response.data["detail"]
        mock_timesale_service.purchase_time_sale.assert_called_once_with(timesale_id, data)
