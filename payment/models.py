from django.db import models
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from product.models import Product
from django.utils import timezone


class ShipingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shiping_full_name = models.CharField(max_length=50)
    shiping_phone = PhoneNumberField(region='IR', blank=True,null=True, unique=True)
    shiping_address = models.TextField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = 'ShipingAddresses'
    
    def __str__(self):
        return f'Shiping Address from{self.shiping_full_name}'
    
class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('posted', 'Posted'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True)
    address = models.TextField(max_length=200, blank=True)
    phone = PhoneNumberField(region='US', blank=True, null=True)
    amount_paid = models.DecimalField(decimal_places=0, max_digits=12)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS, default='pending')
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def str(self):
        return f'order by {self.full_name}'
    
    def save(self, *args, **kwargs):
        if self.user and self.user.profile and not self.full_name:
            profile = self.user.profile
            self.full_name = f"{profile.first_name} {profile.last_name}"
            self.address = profile.address
            self.phone = profile.phone
            
        if self.pk:
            old_status = Order.objects.get(id=self.pk).status
            if old_status != self.status:
                self.update = timezone.now()
        super().save(*args, **kwargs)
        
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=0, max_digits=12)

    def __str__(self):
        return f'order item - {self.product.name} by {self.user.username}'
    
    @property
    def get_total(self):
        return self.price * self.quantity




