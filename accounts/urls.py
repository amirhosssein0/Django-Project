from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CleanLogoutView.as_view(), name='logout'),
    path('logout/confirm/', CustomLogoutView.as_view(), name='logout_confirm'),
    path('signup/', signup_view, name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('password/change/', ChangePasswordView.as_view(), name='password_change'),
    path('delete/account/', DeleteAccountView.as_view(), name='delete_account'),
    path('password/reset/', CustomPasswordReset.as_view(), name='password_reset'),
    path('password/reset/done/', CustomPasswordDone.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', CustomPasswordComplete.as_view(), name='password_reset_complete'),

    
    
]
