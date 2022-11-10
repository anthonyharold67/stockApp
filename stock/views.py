from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from .permissions import CustomModelPermission
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Purchases,
    Sales
)

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    FirmSerializer,
    PurchaseSerializer,
    SalesSerializer,
    CategoryProductsSerializer
)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['name']

    def get_serializer_class(self):
        if self.request.query_params.get('name'):
            return CategoryProductsSerializer
        else:
            return super().get_serializer_class()


class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']


class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PurchaseView(viewsets.ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['firm','product']
    search_fields = ['firm']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        purchase = request.data
        product= Product.objects.get(id=purchase["product_id"])
        product.stock += purchase["quantity"]
        product.save()
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        purchase = request.data
        product= Product.objects.get(id=instance.product_id)
        if purchase["quantity"] == instance.quantity:
            product.stock +=0
        elif purchase["quantity"] != instance.quantity: 
            if purchase["quantity"] > instance.quantity:
                product.stock += purchase["quantity"] - instance.quantity
            else:
                product.stock -= instance.quantity - purchase["quantity"]
        product.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product = Product.objects.get(id=instance.product_id)
        product.stock -= instance.quantity
        product.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class SalesView(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand','product']
    search_fields = ['brand']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        purchase = request.data
        product= Product.objects.get(id=purchase["product_id"])
        product.stock -= purchase["quantity"]
        product.save()
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        purchase = request.data
        product= Product.objects.get(id=instance.product_id)
        if purchase["quantity"] == instance.quantity:
            product.stock +=0
        elif purchase["quantity"] != instance.quantity: 
            if purchase["quantity"] > instance.quantity:
                product.stock -= purchase["quantity"] - instance.quantity
            else:
                product.stock += instance.quantity - purchase["quantity"]
        product.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product = Product.objects.get(id=instance.product_id)
        product.stock += instance.quantity
        product.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    
