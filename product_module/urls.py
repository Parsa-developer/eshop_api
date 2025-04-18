from django.urls import  path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<str:cat>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/comments', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('brands/', views.BrandCreateView.as_view(), name='brand-list'),
    path('categories/', views.CategoryCreateView.as_view(), name='category-list'),
    path('colors/', views.ColorCreateView.as_view(), name='color-list'),
    path('storages/', views.StorageCreateView.as_view(), name='storage-list'),
    path('cart/', views.ShoppingCartAPIView.as_view(), name='shopping-cart'),
    path('cart/items/<int:pk>', views.CartItemUpdateView.as_view(), name='cart-item-update'),
    path('cart/items/<int:pk>/delete/', views.CartItemDeleteView.as_view(), name='cart-item-delete')
]