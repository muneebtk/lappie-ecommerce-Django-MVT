from django.db import models
from category . models import Category
from django.urls import reverse
from user.models import user

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    images = models.ImageField(upload_to = 'photos/products')
    image1 = models.ImageField(upload_to = 'photos/products',blank=True,null=True)
    image2 = models.ImageField(upload_to = 'photos/products',blank=True,null=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    def get_url(self):
        return reverse( 'product_detail',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id




class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice = (
    ('size','size'),
)
variation_value = (
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100,choices=variation_value)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()


    def __str__(self):
        return self.variation_value


class CartItem(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price*self.quantity

    def __unicode__(self):
        return self.product

class Wishlist(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name

class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name

class HomeCarousel(models.Model):
    image = models.ImageField(upload_to='photos/home',)
    main_text = models.TextField(max_length=100)
    sub_text = models.TextField(max_length=200)

    def __str__(self):
        return self.main_text

class Coupons(models.Model):
    coupon_name = models.CharField(max_length=20,unique=True)
    discount_amount = models.IntegerField()
    limit = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coupon_name

class CouponUser(models.Model):
    cur_user = models.ForeignKey(user,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.coupon)

