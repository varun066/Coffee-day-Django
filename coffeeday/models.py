import os
from django.db import models
from django.conf import settings
from min_proj import settings

from django.contrib.auth.models import User

# Create your models here.



class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('coffee', 'Coffee'),
        ('sandwich', 'Sandwich'),
        ('pastry', 'Pastry'),
    ]
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) 
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username} created on {self.created_at}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in cart"
    
class PastOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username} on {self.created_at}"

class PastOrderItem(models.Model):
    past_order = models.ForeignKey(PastOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in order {self.past_order.id}"
    
class QA(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.question