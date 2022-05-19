import uuid as uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    phone_number = models.CharField(max_length=20, default=None)
    address = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    zip_code = models.CharField(max_length=10, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['phone_number', 'address', 'city', 'state', 'zip_code', 'first_name', 'last_name', 'email', 'password']


class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    status = [['Available', 'Available'], ['Rented', 'Rented'], ['Reserved', 'Reserved']]
    status = models.CharField(max_length=10, choices=status, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.item.name


class SafeConduct(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.rental.user.username + ' ' + self.rental.item.name


class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.message


class DeliveryMethod(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

