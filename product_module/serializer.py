from rest_framework import serializers
from .models import Product, ProductBrand, ProductCategory, ProductColor, ProductStorageOption


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ['id', 'title']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'title']

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStorageOption
        fields = ['id', 'capacity']

class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field='title', queryset=ProductBrand.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='title', many=True, queryset=ProductCategory.objects.all()
    )
    colors = serializers.SlugRelatedField(
        slug_field='title', many=True, queryset=ProductColor.objects.all()
    )
    storages = serializers.SlugRelatedField(
        slug_field='capacity', many=True, queryset=ProductStorageOption.objects.all()
    )

    class Meta:
        model = Product
        fields = '__all__'

    def validate_texts(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Must be a list of strings.")
        for item in value:
            if not isinstance(item, str):
                raise serializers.ValidationError(f"'{item}' is not a string.")
        return value

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        colors = validated_data.pop('colors', [])
        storages = validated_data.pop('storages', [])

        product = Product.objects.create(**validated_data)
        product.category.set(categories)
        product.colors.set(colors)
        product.storages.set(storages)
        return product
    

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['colors'] = [color.title for color in instance.colors.all()]
        data['brand'] = instance.brand.title if instance.brand and instance.brand.is_active else None
        data['category'] = [category.title for category in instance.category.all() if category.is_active]
        data['storages'] = [storage.capacity for storage in instance.storages.all()]
        return data