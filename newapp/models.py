from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category

class Product(models.Model):
   
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2X Large'),
    ]

    name = models.CharField(max_length=255, help_text="The name of the product.")
    brand = models.CharField(max_length=255, help_text="The brand of the product.")
    description = models.TextField(blank=True, help_text="A detailed description of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product.")
    stock = models.PositiveIntegerField(default=0, help_text="The number of items available in stock.")
    category = models.ManyToManyField(Category, related_name='products')
    size = models.CharField(max_length=50, blank=True, help_text="The size of the product (e.g., S, M, L, XL).")
    color = models.CharField(max_length=50, blank=True, help_text="The color of the product.")
    material = models.CharField(max_length=100, blank=True, help_text="The material of the product.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the product was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the product was last updated.")
    is_active = models.BooleanField(default=True, help_text="Indicates if the product is active and available for sale.")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="An image of the product.")

    def _str_(self):
        return self.name  

    
class Order(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'live'),(DELETE,'delete'))
    CART_STAGE=0
    ORDER_CONFIRMED=1
    ORDER_PROCESSED=2
    ORDER_DELIVERED=3
    ORDER_REJECTED=4
    STATUS_CHOICE=((ORDER_PROCESSED,'ORDER_PROCESSED'),
                   (ORDER_DELIVERED,'ORDER_DELIVERED'),
                   (ORDER_REJECTED,'ORDER_REJECTED'),
                  
                   )
    order_status = models.IntegerField(choices=STATUS_CHOICE, default=ORDER_PROCESSED)
    owner = models.ForeignKey('Customer', on_delete=models.SET_NULL,null=True, related_name='ordered_items')
    delete_status = models.IntegerField(choices=STATUS_CHOICE, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class OrderedItem(models.Model):
    product = models.ForeignKey('Product', related_name='added_carts',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='added_items')

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
    image=models.ImageField(upload_to='profilepic',null=True,blank=True)
   


    def _str_(self):
        return str(self.user)      
   







   
