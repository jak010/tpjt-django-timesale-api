from rest_framework import serializers


class ProductCreateRequestDto:
    """ 상품 생성 요청 """

    name = serializers.CharField(allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    description = serializers.CharField(allow_null=False)
