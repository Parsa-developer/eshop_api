from django.urls import  path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<str:cat>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('brands/', views.BrandCreateView.as_view(), name='brand-list'),
    path('categories/', views.CategoryCreateView.as_view(), name='category-list'),
    path('colors/', views.ColorCreateView.as_view(), name='color-list'),
    path('storages/', views.StorageCreateView.as_view(), name='storage-list'),
    path('cart/', views.ShoppingCartAPIView.as_view()),
    path('cart/items/', views.CartItemCreateAPIView.as_view()),
    path('cart/items/<int:id>', views.CartItemUpdateDestroyAPIView.as_view())
]