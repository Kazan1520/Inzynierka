import django_filters
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db.models import Q
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework_recursive.fields import RecursiveField

from rental_service.models import *
import re


class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField(required=True, write_only=True, max_length=10)
    first_name = serializers.CharField(required=True, write_only=True, max_length=50)
    last_name = serializers.CharField(required=True, write_only=True, max_length=50)

    def validate_first_name(self, value):
        if not re.match(r'^[a-ząćęłńóśźżA-ZĄĘŁŃÓŚŹŻ\s,]*$', value):
            raise serializers.ValidationError("Invalid first name")
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[a-ząćęłńóśźżA-ZĄĘŁŃÓŚŹŻ\s,]*$', value):
            raise serializers.ValidationError("Invalid last name")

    def validate_phone_number(self, value):
        if not re.match(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', value):
            raise serializers.ValidationError("Phone number must be numeric")
        return value

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(**self.cleaned_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('id', 'image')


class ItemImageSaveSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ItemImage
        fields = ('image', )


class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'status', 'description', 'images', 'category', 'serial_number')


class ItemSaveSerializer(WritableNestedModelSerializer):
    images = ItemImageSaveSerializer(many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'images', 'category', 'serial_number')


class RentalSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = ('id', 'user', 'item', 'start_date', 'end_date', 'status')


class CategoryItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'category')


class ItemRentSerializer(serializers.ModelSerializer):
    rental = RentalSerializer(many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'rental')


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff')
