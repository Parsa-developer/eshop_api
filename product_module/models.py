from django.db import models
from account_module.models import User

# Create your models here.

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.customer.first_name + " " + self.city

class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone_number

class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=200, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"( {self.title} - {self.url_title} )"

class ProductBrand(models.Model):
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=200, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ProductStorageOption(models.Model):
    capacity = models.CharField(max_length=20)

    def __str__(self):
        return self.capacity

class ProductColor(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=200)
    images = models.JSONField(help_text="List of image urls")
    category = models.ManyToManyField(ProductCategory, related_name='product_categories')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    inventory = models.IntegerField(default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    colors = models.ManyToManyField(ProductColor, related_name='product_colors')
    storages = models.ManyToManyField(ProductStorageOption, related_name='product_storages', null=True, blank=True)
    description = models.TextField()
    screen_size = models.FloatField(null=True, blank=True)
    cpu = models.CharField(max_length=100, null=True, blank=True)
    cores = models.PositiveIntegerField(null=True, blank=True)
    main_camera = models.CharField(max_length=100, null=True, blank=True)
    front_camera = models.CharField(max_length=100, null=True, blank=True)
    battery_capacity = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    delivery_info = models.CharField(max_length=100, null=True, blank=True)
    warranty = models.CharField(max_length=100, null=True, blank=True)
    screen_resolution = models.CharField(max_length=100, null=True, blank=True)
    screen_refresh_rate = models.PositiveIntegerField(null=True, blank=True)
    pixel_density = models.PositiveIntegerField(null=True, blank=True)
    screen_type = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    last_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

