from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'Turkish')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name'
        )


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'category_id',
            'brand',
            'brand_id',
            'stock'
        )

        read_only_fields = ('stock',)


class CategoryProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'name',
            'products'
        )


class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            'id',
            'name',
            'phone',
            'address'
        )


class TransactionSerializer(serializers.ModelSerializer):
    createds=serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    time_hour = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'user',
            'firm',
            'firm_id',
            'transaction',
            'product',
            'product_id',
            'quantity',
            'price',
            'price_total',
            "created",
            "createds",
            "time_hour"
        )

        read_only_fields = ('price_total',)

    def validate(self, data):
        if data.get('transaction') == 0:
            product = Product.objects.get(id=data.get('product_id'))
            if data.get('quantity') > product.stock:
                raise serializers.ValidationError(
                    f'Dont have enough stock. Current stock is {product.stock}'
                )
        return data
    def get_createds(self,obj):
        return datetime.datetime.strftime(obj.created,'%d.%m.%Y')
    def get_time_hour(self,obj):
        return datetime.datetime.strftime(obj.created,'%X')
