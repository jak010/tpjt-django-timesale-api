from rest_framework import serializers

from apps.models import Product


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price', 'description']


class CreateProductRequestDto(serializers.Serializer):
    name = serializers.CharField(allow_null=True, allow_blank=True)
    price = serializers.IntegerField(allow_null=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)


class CreateProductResponseDto(serializers.Serializer):
    data = ProductModelSerializer()


class ProductListDto:
    class Response(serializers.Serializer):
        data = ProductModelSerializer(many=True)
