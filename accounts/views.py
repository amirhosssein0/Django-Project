from django.shortcuts import render, redirect
from django.contrib.auth import  login, logout
from .forms import LoginForm, SignupForm, UpdateUser, UpdateProfile
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from payment.models import Order


class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('product:products')
    success_message = "Login Successfully"
    

    
class CustomLogoutView(generic.TemplateView):
    template_name = 'accounts/logout_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel'] = self.request.GET.get('cancel')
        return context
    
    
class CleanLogoutView(LogoutView):
    next_page = reverse_lazy('product:products')

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Logout Successfully')
        return response

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,('Signup Successfully'))
            return redirect('product:products')
        else:
            messages.error(request, ('There Is A Problem'))
            return redirect('accounts:signup')
            
    else:
        form = SignupForm()
        
    return render(request, 'accounts/signup.html', {'form':form})


class ProfileView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        orders = Order.objects.filter(user=user).order_by('-date_ordered')
        posted_orders = Order.objects.filter(status = 'posted')
        other_orders = orders.exclude(status = 'posted')
        context.update({
            'posted_orders':posted_orders,
            'other_orders':other_orders,
            'total_orders':orders.count()
        })
        return context
    
    
class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'accounts/update_profile.html'
    form_class = UpdateUser
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = UpdateProfile(instance=self.request.user.profile)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = UpdateProfile(
            request.POST, 
            request.FILES, 
            instance=self.request.user.profile
        )
        
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)
    
    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        messages.success(self.request, 'Profile Update Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form, profile_form):
        messages.error(self.request, 'There IS A Problem.Please Try Again')
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )
    
class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('product:products')
    

class CustomPasswordReset(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password reset link sent to your email")
        return response

class CustomPasswordDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been updated successfully")
        return response

class CustomPasswordComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    
class DeleteAccountView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('product:products')
    
    def get_object(self, queryset = None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        messages.success(request, 'Account Delete Successfully')
        return response
    







