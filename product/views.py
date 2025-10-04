from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Product, Category, Comment, Color
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages

class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 1
    ordering = ['-created_at']  # Add ordering to fix pagination warning
        
class CategoryProductListView(ListView):
    model = Product  
    template_name = 'products/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category, is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['newarrivals'] = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
        context['comments'] = Comment.objects.filter(product=self.object).order_by('-created_at')
        context['form'] = CommentForm()
        context['colors'] = Color.objects.filter(product=product)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.product = self.object
            comment.author = request.user
            comment.save()
        return self.get(request, *args, **kwargs)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'products/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.object.product.slug})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'products/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.object.product.slug})

class SearchView(View):
    template_name = 'products/search.html'

    def post(self, request, *args, **kwargs):
        searched = request.POST.get('searched')
        searched = Product.objects.filter(Q(name__icontains=searched)|Q(description__icontains=searched))

        if not searched:
            messages.error(request, 'No Results Found')
            return render(request, self.template_name, {})

        else:
            context = {'searched':searched}
            return render(request, self.template_name, context)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
class FavouritesView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        
        if product.favourites.filter(id=request.user.id).exists():
            product.favourites.remove(request.user)
            messages.success(request, 'Remove From Favorites')
        else:
            product.favourites.add(request.user)
            messages.success(request, 'Add To Favorites')
            
        return redirect(reverse('product:product_detail', kwargs={'slug': slug})) 

class ProductFavouritesView(LoginRequiredMixin, View):
    def get(self, request):
        favourites = request.user.favourites.all()
        context = {'favourites': favourites}
        return render(request, 'products/favouritelist.html', context)  

    
    
    