from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rental_service.models import *
from rental_service.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/<int:pk>/', UserViewSetDetail.as_view(), name='user_detail'),
    path('api/user/', UserViewSetList.as_view(), name='user_list'),
    path('api/item/<int:pk>/', ItemViewSetDetail.as_view(), name='item_detail'),
    path('api/item/', ItemViewSetList.as_view(), name='item_list'),
    path('api/item/<int:pk>/rent/', ItemRentViewSetList.as_view(), name='rent_list'),

]
