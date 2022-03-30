from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from rental_service.models import *
import re

class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField(required=True, write_only=True, max_length=10)
    address = serializers.CharField(required=True, write_only=True, max_length=100)
    city = serializers.CharField(required=True, write_only=True, max_length=50)
    state = serializers.CharField(required=True, write_only=True, max_length=50)
    zip_code = serializers.CharField(required=True, write_only=True, max_length=10)
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

    def validate_zip_code(self, value):
        if not re.match(r'^[0-9]{2}-[0-9]{3}$', value):
            raise serializers.ValidationError("Invalid zip code")
        return value

    def validate_address(self, value):
        if not re.match(r'^[a-ząćęłńóśźżA-ZĄĘŁŃÓŚŹŻ0-9\s,]*$', value):
            raise serializers.ValidationError("Invalid address")
        return value

    def validate_city(self, value):
        if not re.match(r'^[a-ząćęłńóśźżA-ZĄĘŁŃÓŚŹŻ0-9\s,]*$', value):
            raise serializers.ValidationError("Invalid city")
        return value

    def validate_state(self, value):
        if not re.match(r'^[a-ząćęłńóśźżA-ZĄĘŁŃÓŚŹŻ0-9\s,]*$', value):
            raise serializers.ValidationError("Invalid state")
        return value

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'address': self.validated_data.get('address', ''),
            'city': self.validated_data.get('city', ''),
            'state': self.validated_data.get('state', ''),
            'zip_code': self.validated_data.get('zip_code', ''),
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(**self.cleaned_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):
    parentCategory = serializers.PrimaryKeyRelatedField()
    subcategories = serializers.ListSerializer(child=RecursiveField())

    class Meta:
        model = Category
        fields = ('parentCategory', 'id', 'name', 'subcategories')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price', 'image', 'category')


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'user', 'item', 'start_date', 'end_date', 'status')


class SafeConductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeConduct
        fields = ('id', 'user','item', 'document')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'item', 'rating', 'comment')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user', 'message')


class UserMessagesSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True)

    class Meta:
        model = Message
        fields = ('id', 'user', 'message')


class CategoryItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'category', 'items')



