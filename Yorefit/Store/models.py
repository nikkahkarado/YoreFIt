from email.policy import default
import imp
from itertools import product
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    stars = models.PositiveIntegerField(default=1)
    fit_type = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    colors = models.CharField(max_length=100)
    sizes = models.CharField(max_length=50)
    features = models.TextField()
    stock = models.IntegerField()
    img = models.ImageField(upload_to='store/product_images')
    publish_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id}. {self.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/product_images')

    def __str__(self):
        return f'Image: {self.product.name}'


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    json_field = models.CharField(max_length=99999)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    address = models.TextField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.IntegerField()
    contact = models.IntegerField()
    email = models.EmailField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    delivery = models.CharField(max_length=10)
    payment = models.CharField(max_length=10)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.email} -{self.time}'


class OrderUpdate(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    steps = [
        (1, 'Order Placed'),
        (2, 'Shipped to warehouse'),
        (3, 'Packaging complete'),
        (4, 'Arrived to your country'),
        (5, 'Delivered!')
    ]
    progress = models.IntegerField(choices=steps, default=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order: {self.order.order_id} -Step:{self.progress}'
    
    
class Review(models.Model):
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    title = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(default="No reviews")
    time = models.DateField(auto_now_add=True)
    def __str__(self):
            return f'{self.stars}Stars {self.title} -{self.user.first_name + self.user.last_name}'


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
