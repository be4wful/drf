from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=120)
    fio = models.CharField(max_length=120)
    email = models.EmailField(max_length=120, unique=True)
    password = models.CharField(validators=[MinLengthValidator(4)], blank=False, max_length=120)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username']

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    products = models.ManyToManyField(Product, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.products} {self.user.email}'


class Order(models.Model):
    products = models.ManyToManyField(Product)
    order_price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email