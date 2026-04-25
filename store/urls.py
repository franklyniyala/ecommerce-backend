from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, CartView, CartItemUpdateDeleteView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/<int:item_id>/', CartItemUpdateDeleteView.as_view(), name='cart-item-update-delete'),
]
