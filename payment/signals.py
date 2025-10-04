from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Order



@receiver(pre_save, sender=Order)
def pre_save_order_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.full_name)
    exist = Order.objects.filter(slug=slug).exists()
    if exist:
        slug = '%s-%s' %(slug, instance.id)
    instance.slug = slug