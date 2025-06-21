from rest_framework import serializers


class CreateProductRequestDto(serializers.Serializer):
    name = serializers.CharField(allow_null=True, allow_blank=True)
    price = serializers.IntegerField(allow_null=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)
