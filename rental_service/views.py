from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rental_service.serializers import *


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
