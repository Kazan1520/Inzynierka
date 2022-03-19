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

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['phone_number', 'address', 'city', 'state', 'zip_code', 'first_name', 'last_name', 'email', 'password']