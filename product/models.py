from django.db import models
from django.urls import reverse
from accounts.models import User


class Category(models.Model):
    category = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.category
    
        
class Product(models.Model):    
    name = models.CharField(max_length=50)
    description = models.TextField()
    info = models.CharField(max_length=250, default='info')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tumbnail = models.ImageField(upload_to='tumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    favourites = models.ManyToManyField(User, related_name='favourites', blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"slug": self.slug})

        
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("product:product_detail")

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='covers/')
    
    def __str__(self):
        return self.product.name
    
class Color(models.Model):
    color = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  blank=True, null=True, related_name='color')

    def __str__(self):
        return self.color
    
    

