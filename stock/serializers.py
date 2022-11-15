from unicodedata import category
from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Purchases,
    Sales
)
from rest_framework.serializers import raise_errors_on_nested_writes
import traceback
from rest_framework.utils import model_meta
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
    
    # def validate_name(self,value):
    #     if value and Category.objects.filter(name__exact=value).exists():
    #         raise serializers.ValidationError("Name already exists!")   
    #     return value
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
    # def validate_name(self,value):
    #     if value and Brand.objects.filter(name__exact=value).exists():
    #         raise serializers.ValidationError("Name already exists!") 
    #     return value


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
    
    # def validate_name(self,value):
    #     if value and Product.objects.filter(name__exact=value).exists():
    #         raise serializers.ValidationError("Name already exists!") 
    #     return value


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
    # def validate_name(self,value):
    #     if value and Firm.objects.filter(name__exact=value).exists():
    #         raise serializers.ValidationError("Name already exists!") 
    #     return value

class PurchaseSerializer(serializers.ModelSerializer):
    createds=serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    time_hour = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Purchases
        fields = (
            'id',
            'user',
            'firm',
            'firm_id',
            'brand',
            'brand_id',
            'product',
            'product_id',
            'quantity',
            'category',
            'price',
            'price_total',
            "created",
            "createds",
            "time_hour"
        )

        read_only_fields = ('price_total',)

    def get_createds(self,obj):
        return datetime.datetime.strftime(obj.created,'%d.%m.%Y')
    def get_time_hour(self,obj):
        return datetime.datetime.strftime(obj.created,"%H:%M") 
    def get_category(self,obj):
        products = Product.objects.filter(id=obj.product_id).values()
        category_id= products[0]['category_id']
        return list(Category.objects.filter(id=category_id).values())
    

class SalesSerializer(serializers.ModelSerializer):
    createds=serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    time_hour = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = (
            'id',
            'user',
            'brand',
            'brand_id',
            'product',
            'product_id',
            'quantity',
            'price',
            'price_total',
            "created",
            'category',
            "createds",
            "time_hour"
        )

        read_only_fields = ('price_total',)

    def validate(self, data):
        product = Product.objects.get(id=data.get('product_id'))
        if data.get('quantity') > product.stock:
            raise serializers.ValidationError(f'Dont have enough stock. Current stock is {product.stock}')
        return data
    def get_createds(self,obj):
        return datetime.datetime.strftime(obj.created,'%d.%m.%Y')
    def get_time_hour(self,obj):
        return datetime.datetime.strftime(obj.created,"%H:%M")
    def get_category(self,obj):
        products = Product.objects.filter(id=obj.product_id).values()
        category_id= products[0]['category_id']
        return list(Category.objects.filter(id=category_id).values())


# class TransactionSerializer(serializers.ModelSerializer):
#     createds=serializers.SerializerMethodField()
#     user = serializers.StringRelatedField()
#     firm = serializers.StringRelatedField()
#     firm_id = serializers.IntegerField()
#     brand = serializers.StringRelatedField()
#     brand_id = serializers.IntegerField()
#     product = serializers.StringRelatedField()
#     product_id = serializers.IntegerField()
#     time_hour = serializers.SerializerMethodField()


#     class Meta:
#         model = Transaction
#         fields = (
#             'id',
#             'user',
#             'firm',
#             'firm_id',
#             'brand',
#             'brand_id',
#             'transaction',
#             'product',
#             'product_id',
#             'quantity',
#             'price',
#             'price_total',
#             "created",
#             "createds",
#             "time_hour"
#         )

#         read_only_fields = ('price_total',)

#     def validate(self, data):
#         if data.get('transaction') == 0:
#             product = Product.objects.get(id=data.get('product_id'))
#             if data.get('quantity') > product.stock:
#                 raise serializers.ValidationError(
#                     f'Dont have enough stock. Current stock is {product.stock}'
#                 )
#         return data
#     def get_createds(self,obj):
#         return datetime.datetime.strftime(obj.created,'%d.%m.%Y')
#     def get_time_hour(self,obj):
#         return datetime.datetime.strftime(obj.created,"%H:%M")
