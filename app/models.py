from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES=(
    ('Delhi','Delhi'),
    ('Mumbai','Mumbai'),
    ('Gujrat','Gujrat'),
    ('Maharashtra','Maharashtra'),
    ('Chennai','Chennai'),
    ('Punjab','Punjab'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh')
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def _str_(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('M','MOBILES'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear')
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')
    
    def _str_(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price