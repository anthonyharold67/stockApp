from django.db.models.signals import pre_save, post_save,m2m_changed
from django.dispatch import receiver
from .models import Purchases, Product,Sales
from django.shortcuts import get_object_or_404


@receiver(pre_save, sender=Purchases)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.quantity * instance.price

@receiver(pre_save, sender=Sales)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.quantity * instance.price

# @receiver(pre_save, sender=Purchases)
# def update_stock_purchase(sender, instance, **kwargs):
#     product = get_object_or_404(Product,id=instance.product_id)
#     purchase  =get_object_or_404(Purchases, id = instance.id)
#     if purchase:
#         if instance.quantity == purchase.quantity:
#             if not product.stock:
#                 product.stock = instance.quantity
#             else:
#                 product.stock += 0
#         else:
#             if not product.stock:
#                 product.stock = instance.quantity
#             else:
#                 product.stock += instance.quantity - purchase.quantity
#         product.save()

# @receiver(post_save, sender=Purchases)
# def update_stock(sender, instance, **kwargs):
#     product = Product.objects.get(id=instance.product_id)
#     if not product.stock:
#         product.stock = instance.quantity
#     else:
#         product.stock += instance.quantity
#     product.save()

# @receiver(post_save, sender=Sales)
# def update_stock(sender, instance, **kwargs):
#     product = Product.objects.get(id=instance.product_id)
#     product.stock -= instance.quantity
#     product.save()
