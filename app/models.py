from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
STATE_CHOICES = (
    ('Gujarat', 'Gujarat'),
    ('Maharashtra', 'Maharashtra'),
    ('Karnataka', 'Karnataka'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Haryana', 'Haryana'),
    ('Punjab', 'Punjab'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
    ('Kerala', 'Kerala'),
    ('Bihar', 'Bihar'),
    ('Rajasthan', 'Rajasthan'),
    ('Odisha', 'Odisha'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50, choices=STATE_CHOICES)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('L', 'Laptop'),
    ('M', 'Mobile'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)


class Product(models.Model):
    title = models.CharField(max_length=20)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=40)
    product_image = models.ImageField(upload_to='productimg')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Pending")
