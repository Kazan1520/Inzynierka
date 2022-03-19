from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rental_service.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
]
