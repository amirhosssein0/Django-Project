from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CategoryProductListView,
    CommentUpdateView,
    CommentDeleteView,
    SearchView,
    FavouritesView,
    ProductFavouritesView
)

app_name = 'product'
urlpatterns = [
    path('favourite/<slug:slug>/', FavouritesView.as_view(), name='favourite_product'),
    path('favourites/list/', ProductFavouritesView.as_view(), name='favourite_list'), 
    path('search/', SearchView.as_view(), name='search'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/<slug:slug>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<slug:slug>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('category/<slug:slug>/', CategoryProductListView.as_view(), name='category_product'),
    path('', ProductListView.as_view(), name='products'),
]