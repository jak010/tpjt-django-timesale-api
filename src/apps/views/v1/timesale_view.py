from __future__ import annotations

from typing import TYPE_CHECKING

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dto.timsale_dto import TimeSaleCreateRequestDto, TimeSaleDetailResponseDto, TimeSaleOngoingResponseDto, TimeSalePurchaseRequestDto
from apps.services.v1.timesale_service import TimeSaleService

if TYPE_CHECKING:
    from apps.services.interfaces import ITimeSaleService


class TimeSaleView(APIView):
    service: ITimeSaleService = TimeSaleService()

    @extend_schema(
        tags=["타임세일"],
        summary="타임세일 생성",
        description="타임세일 생성 API",
        request=TimeSaleCreateRequestDto,
        responses={201: None},
    )
    def post(self, request):
        """ 타임세일 생성하기 """
        serializer = TimeSaleCreateRequestDto(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.create_timesale(serializer)
        return Response(status=status.HTTP_201_CREATED)


class TimeSaleDetailView(APIView):
    service: ITimeSaleService = TimeSaleService()

    @extend_schema(
        tags=["타임세일"],
        summary="타임세일 상세 조회",
        description="타임세일 상세 조회 API",
        responses={200: TimeSaleDetailResponseDto},
    )
    def get(self, request, timesale_id: int):
        """ 타임세일 정보 상세조회하기 """
        timesale = self.service.get_timesale(timesale_id)
        return Response(TimeSaleDetailResponseDto(timesale).data, status=status.HTTP_200_OK)


class TimeSaleOngoingView(APIView):
    service: ITimeSaleService = TimeSaleService()

    @extend_schema(
        tags=["타임세일"],
        summary="진행중인 타임세일 조회",
        description="진행중인 타임세일 조회 API",
        responses={200: TimeSaleOngoingResponseDto(many=True)},
    )
    def get(self, request):
        """ 진행중인 타임세일 정보 조회하기 """
        timesales = self.service.get_ongoing_timesales(page=1, size=10)
        return Response(TimeSaleOngoingResponseDto(timesales, many=True).data, status=status.HTTP_200_OK)


class TimeSaleOrderView(APIView):
    service: ITimeSaleService = TimeSaleService()

    @extend_schema(
        tags=["타임세일"],
        summary="타임세일 구매",
        description="타임세일 구매 API",
        request=TimeSalePurchaseRequestDto,
        responses={201: None},
    )
    def post(self, request, timesale_id: int):
        """ 타임세일 구매하기 """
        serializer = TimeSalePurchaseRequestDto(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.service.purchase_time_sale(timesale_id, serializer)
        return Response(status=status.HTTP_201_CREATED)
