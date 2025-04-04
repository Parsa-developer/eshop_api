from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, ProductStorageOption, ProductBrand, ProductCategory, ProductColor
from .serializer import ProductSerializer, ProductDetailSerializer, BrandSerializer, CategorySerializer, ColorSerializer, StorageSerializer

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
