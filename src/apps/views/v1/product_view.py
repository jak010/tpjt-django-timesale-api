from __future__ import annotations

from typing import TYPE_CHECKING

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.services.v1.product_service import ProductService
from apps.views.request.product_dto import CreateProductRequestDto, CreateProductResponseDto, ProductListDto

if TYPE_CHECKING:
    from apps.services.interfaces import IProductService


class ProductView(APIView):
    service: IProductService = ProductService()

    @extend_schema(
        tags=["V1-PRODUCT"],
        operation_id="V1-PRODUCT-LIST",
        description="포인트 적립하기",
        parameters=None,
        responses={
            200: ProductListDto.Response
        }
    )
    def get(self, request):
        """ 상품 목록조회
        """

        products = self.service.get_all_products()

        response_data = ProductListDto.Response({"data": products})

        return Response(
            response_data.data,
            status=200
        )

    @extend_schema(
        tags=["V1-PRODUCT"],
        operation_id="V1-PRODUCT-CREATE",
        description="상품 생성하기",
        request=CreateProductRequestDto,
        responses={
            200: CreateProductResponseDto
        }
    )
    def post(self, request):
        """ 상품 생성하기
        """

        command = CreateProductRequestDto(data=request.data)
        command.is_valid()

        product = self.service.create_product(command=command)

        response_data = CreateProductResponseDto({"data": product})
        return Response(
            response_data.data,
            status=201
        )
