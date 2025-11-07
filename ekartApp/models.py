from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    image=models.ImageField(upload_to='media/category/')

    def __str__(self):
        return self.category_name

class Products(models.Model):
    product_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.PositiveBigIntegerField()
    image=models.ImageField(upload_to='media')
    description=models.TextField(max_length=200)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,default='in-cart',choices=(('in-cart','In-Cart'),('order-placed','Order-Placed')))
    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
    


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Product=models.ForeignKey(Cart,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    shipping_address=models.TextField(max_length=200)
    contact_number=models.CharField(max_length=15)
    status=models.CharField(max_length=50,default='order-placed',choices=(('order-placed','Order-Placed'),('canceled','Canceled'),('shipped','Shipped'),('delivered','Delivered')))
    expected_delivery_date=models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"