from unicodedata import category
from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)
import datetime


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'product_count'
        )
    
    def get_product_count(self,obj):
        return Product.objects.filter(category_id=obj.id).count()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'image'

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
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'name',
            'products',
            'product_count'
        )
    
    def get_product_count(self,obj):
        return Product.objects.filter(category_id=obj.id).count()


class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            'id',
            'name',
            'phone',
            'image',
            'address'
        )


class TransactionSerializer(serializers.ModelSerializer):
    createds=serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
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
            'brand',
            'brand_id',
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
        return datetime.datetime.strftime(obj.created,"%H:%M")
