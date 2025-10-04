from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Product, Category, Comment



@receiver(pre_save, sender=Product)
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    exist = Product.objects.filter(slug=slug).exists()
    if exist:
        slug = '%s-%s' %(slug, instance.id)
    instance.slug = slug
    

@receiver(pre_save, sender=Category)
def pre_save_category_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.category)
    exist = Category.objects.filter(slug=slug).exists()
    if exist:
        slug = '%s-%s' %(slug, instance.id)
    instance.slug = slug
    
@receiver(pre_save, sender=Comment)
def pre_save_comment_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.comment)
    exist = Comment.objects.filter(slug=slug).exists()
    if exist:
        slug = '%s-%s' %(slug, instance.id)
    instance.slug = slug