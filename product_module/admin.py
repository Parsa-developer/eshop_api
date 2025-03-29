from django.contrib import admin
from .models import Product, ProductBrand, ProductCategory, ProductColor, ProductStorageOption

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_price', 'discounted_price', 'brand', 'inventory', 'is_active']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductBrand)
admin.site.register(ProductCategory)
admin.site.register(ProductColor)
admin.site.register(ProductStorageOption)