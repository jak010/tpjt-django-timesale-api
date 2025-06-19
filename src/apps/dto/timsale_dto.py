from rest_framework import serializers


class TimeSaleCreateRequestDto(serializers.Serializer):
    """ TimeSale 생성요청 """

    product_id = serializers.IntegerField(allow_null=False)
    quantity = serializers.IntegerField(allow_null=False)
    discount_price = serializers.IntegerField(allow_null=False)
    start_at = serializers.DateTimeField(allow_null=False)
    end_at = serializers.DateTimeField(allow_null=False)
