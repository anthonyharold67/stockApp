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
router.register('category', CategoryView)
router.register('brand', BrandView)
router.register('product', ProductView)
router.register('firm', FirmView)
router.register('purchases', PurchaseView)
router.register('sales', SalesView)

urlpatterns = [

] + router.urls
