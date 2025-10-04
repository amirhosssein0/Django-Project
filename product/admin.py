from django.contrib import admin
from .models import Category, Product, Comment, ProductImage, Color


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Color)
admin.site.register(ProductImage)

