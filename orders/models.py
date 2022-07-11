from django.db import models
from store.models import Product
from store.models import user,Variation

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Address(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=8)


    def __str__(self):
        return self.first_name

    def full_name(self):
        return self. first_name +' ' + self.last_name

    def full_address(self):
        return self.address_line_1+' '+ self.address_line_2

class Order(models.Model):
    STATUS = {
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        

    }

    user = models.ForeignKey(user,on_delete=models.SET_NULL,null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=100)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
STATUS={
    ('new','new'),
    ('Delivered','Delivered'),
    ('shipped','shipped'),
    ('cancelled','cancelled'),
}

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS,default='new')


    def __str__(self):
        return self.product.product_name

