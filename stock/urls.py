from django.urls import path
from .views import (
    CategoryView,
    BrandView,
    ProductView,
    FirmView,
    SalesView,
    PurchaseView

)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', CategoryView)
router.register('brands', BrandView)
router.register('products', ProductView)
router.register('firms', FirmView)
router.register('purchases', PurchaseView)
router.register('sales', SalesView)

urlpatterns = [

] + router.urls
