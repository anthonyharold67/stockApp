from django.db.models.signals import pre_save, post_save,m2m_changed
from django.dispatch import receiver
from .models import Purchases, Product,Sales


@receiver(pre_save, sender=Purchases)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.quantity * instance.price

@receiver(pre_save, sender=Sales)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.quantity * instance.price


@receiver(post_save, sender=Purchases)
def update_stock(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product_id)
    if not product.stock:
        product.stock = instance.quantity
    else:
        product.stock += instance.quantity
    product.save()

@receiver(post_save, sender=Sales)
def update_stock(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product_id)
    product.stock -= instance.quantity
    product.save()
