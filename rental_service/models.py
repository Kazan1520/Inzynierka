import uuid as uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from model_clone import CloneMixin


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    phone_number = models.CharField(max_length=20, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rodo = models.BooleanField(default=False)
    terms_of_use = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'email', 'password', 'rodo', 'terms_of_use']


class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(upload_to='images/')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.url


class Item(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    status = [['Available', 'Available'], ['Rented', 'Rented'], ['Reserved', 'Reserved']]
    status = models.CharField(max_length=10, choices=status, default='Available')
    serial_number = models.CharField(max_length=50, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rental(models.Model, CloneMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = [['Awaiting', 'Awaiting'], ['Returned', 'Returned'], ['Not returned', 'Not returned'], ["Rejected", "Rejected"]]
    status = models.CharField(max_length=20, choices=status, default='Awaiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.item.name
