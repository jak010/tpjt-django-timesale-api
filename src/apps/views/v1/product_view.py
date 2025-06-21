from __future__ import annotations

from rest_framework.views import APIView

from typing import TYPE_CHECKING

from apps.services.v1.product_service import ProductService
from apps.views.request.product_dto import CreateProductRequestDto

if TYPE_CHECKING:
    from apps.services.interfaces import IProductService


class ProductView(APIView):
    service: IProductService = ProductService()

    def post(self, request):
        """ 상품 생성하기
        """

        command = CreateProductRequestDto(
            data=request.data
        )
        command.is_valid()

        product = self.service.create_product(
            command=command
        )

        return product
