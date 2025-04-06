# Generated by Django 5.1.7 on 2025-04-06 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0003_cartitem_added_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='shopping_cart',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product_module.shoppingcart'),
            preserve_default=False,
        ),
    ]
