from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, blank=False)
    
    def __str__(self):
        return self.username
    
    def _make_uid_urlsafe(self):
        return urlsafe_base64_encode(force_bytes(self.pk))
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    modified = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    phone = PhoneNumberField(region='US', blank=True,null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar.jpg')
    address = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, 'path'): 
            image = Image.open(self.avatar.path)
            if image.height > 100 or image.width > 100:
                new_image = (100, 100)
                image.thumbnail(new_image)
                image.save(self.avatar.path)

    

    
    
    


    