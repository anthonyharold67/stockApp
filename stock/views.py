from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from .permissions import CustomModelPermission
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SalesView(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand','product']
    search_fields = ['brand']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
