from django.contrib import admin
from .models import Product, ProductImage, Order, OrderUpdate, Review

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(Review)
