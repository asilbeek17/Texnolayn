from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.validators import integer_validator
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=155)
    image1 = models.ImageField(upload_to='Product_image/')
    image2 = models.ImageField(upload_to='Product_image/')
    image3 = models.ImageField(upload_to='Product_image/')
    image4 = models.ImageField(upload_to='Product_image/')
    description = models.TextField()
    category = models.ForeignKey(to='app.Category', on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.product.price * self.quantity


class Blog(models.Model):
    image = models.ImageField(upload_to='blog/')
    title = models.CharField(max_length=155)
    description = models.TextField()
    author = models.ForeignKey(to='app.User',
                               on_delete=models.CASCADE,
                               related_name='blogs')

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a phone number!')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=155, unique=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=25, validators=[integer_validator], null=True, blank=True)
    address = models.CharField(max_length=155, null=True, blank=True)
    # forget_password_token = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Wishlist(models.Model):
    user = models.ForeignKey(to='app.User',
                             on_delete=models.CASCADE,
                             related_name='wishlists')  # kop wishlistlarga bitta user
    product = models.ManyToManyField(to='app.Product',
                                     related_name='wishlists')  # kop productlarga kop wishlist


class Order(models.Model):
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)