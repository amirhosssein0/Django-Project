from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Profile
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='username:', 
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'username'
        }))
    password = forms.CharField(
        label='password:',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'password',
            'type':'password'
        }))
    
    
    
class SignupForm(forms.Form):
    username = forms.CharField(
        label='username', 
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'username'
        }))
    email = forms.EmailField(
        label='email', 
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'email'
        }))
    password = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'password',
            'type':'password'
        }))
    
    password_confirm= forms.CharField(
        label='password_confirm',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'confirm password',
            'type':'password'
        }))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This Username Already Exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This Email Already Exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        password_confirm = cleaned_data["password_confirm"]

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords Does Not Match")
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
        
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user
    
class UpdateUser(forms.ModelForm):
    username = forms.CharField(
    label='username', 
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'username'
    }))
    email = forms.EmailField(
        label='email', 
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'email'
        }))
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'First Name'
    }))
    last_name = forms.CharField(
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Last Name'
    }))
    phone = PhoneNumberField(
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'phone number'
    }),
    region='IR'
    )
    address = forms.CharField(
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'address'
    }))
    avatar = forms.ImageField(
    widget=forms.FileInput(attrs={
        'class':'form-control',
        'placeholder':'avatar'
    }))
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'address', 'avatar']
        

        
    


                

        
    