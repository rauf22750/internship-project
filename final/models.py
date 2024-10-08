from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class product(models.Model):
    p_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    detail = models.TextField()
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.p_name

class ProductImage(models.Model):
    product = models.ForeignKey(product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.p_name}"


class data(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email= models.EmailField(max_length=40)


class samedata(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

class thirddata(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)

class forthdata(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email = models.EmailField(max_length=50)



class cartitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Make sure this is not null
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.p_name} - {self.quantity} x {self.total_price}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    mobile = models.CharField(max_length=50, null=True)
    address = models.TextField()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    STATUS_CHOICES = (
        ('process', 'In Process'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(choices=STATUS_CHOICES, default='process', max_length=150)

    def __str__(self):
        return f"{self.product.p_name} - {self.quantity} x {self.total_price} ({self.get_order_status_display()})"

RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.IntegerField(choices=RATING)
    images = models.JSONField(default=list, blank=True)  # Store image URLs in JSON format


    class Meta:
        verbose_name_plural = 'Reviews'

    def get_review_rating(self):
        return self.review_rating
