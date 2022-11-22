from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rental_service.models import *
from rental_service.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/<str:pk>/', UserViewSetDetail.as_view(), name='user_detail'),
    path('api/user/', UserViewSetList.as_view(), name='user_list'),
    path('api/item/<str:pk>/', ItemViewSetDetail.as_view(), name='item_detail'),
    path('api/item/', ItemViewSetList.as_view(), name='item_list'),
    path('api/item/<str:pk>/rent/', ItemRentViewSetList.as_view(), name='rent_list'),
    path('api/categories/', CategoryViewSetList.as_view(), name='category_list'),
    path('api/categoryitems/<str:pk>/', CategoryItemsViewSetDetail.as_view(), name='category_detail'),
    path('api/itemstoexcel/', GenerateItemExcelView.as_view(), name='items_to_excel'),
    path('api/itemcount/', ItemCountView.as_view(), name='item_count'),
    path('api/categoryitemscount/<str:pk>/', CategoryItemsCountView.as_view(), name='category_items_count'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
