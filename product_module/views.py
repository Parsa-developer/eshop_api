from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Comment, ProductStorageOption, ProductBrand, ProductCategory, ProductColor, ShoppingCart, CartItem
from .serializer import ProductSerializer, CommentSerializer, ProductDetailSerializer, BrandSerializer, CategorySerializer, ColorSerializer, StorageSerializer, ShoppingCartSerializer, CartItemSerializer

# Create your views here.

class ProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        params = request.query_params
        category = kwargs.get('cat', None)
        if category:
            queryset = Product.objects.filter(category__title=category)
        else:
            queryset = Product.objects.filter(is_active=True)

        if brand := params.get('brand'):
            queryset = queryset.filter(brand__title__iexact=brand.strip().lower())
        if battery_capacity := params.get('battery_capacity'):
            queryset = queryset.filter(battery_capacity__exact=int(battery_capacity))
        if screen_type := params.get('screen_type'):
            queryset = queryset.filter(screen_type__iexact=screen_type.strip().lower())
        if screen_size := params.get('screen_size'):
            try:
                queryset = queryset.filter(screen_size=float(screen_size))
            except ValueError:
                return None
        if color := request.query_params.get('color'):
            queryset = queryset.filter(colors__title__iexact=color)
        if storage := request.query_params.get('storage'):
            queryset = queryset.filter(storages__capacity__iexact=storage)
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        try:
            if min_price:
                queryset = queryset.filter(original_price__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(original_price__lte=float(max_price))
        except ValueError:
            pass
        if not queryset.exists():
            return Response([])
        queryset = queryset.distinct()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

class BrandCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ProductBrand.objects.all()
    serializer_class = BrandSerializer

class CategoryCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer

class ColorCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ProductColor.objects.all()
    serializer_class = ColorSerializer

class StorageCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ProductStorageOption.objects.all()
    serializer_class = StorageSerializer

class ShoppingCartAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = ShoppingCart.objects.get_or_create(user=self.request.user)
        return cart
    
    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            cart_serializer = ShoppingCartSerializer(cart)
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cart = cart_item.cart
            cart_serializer = ShoppingCartSerializer(cart)
            return Response(cart_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart = cart_item.cart
        cart_item.delete()
        cart_serializer = ShoppingCartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['slug']
        return Comment.objects.filter(product__slug=product_id)
    
    def perform_create(self, serializer):
        product_id = self.kwargs['slug']
        try:
            product = Product.objects.get(slug=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product Not Found")
        serializer.save(product=product)
