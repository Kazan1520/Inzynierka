from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rental_service.models import *
from rental_service.views import *
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import LoginView, UserDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('account/', include('allauth.urls')),
    path('api/get_self_data/', UserDetailsView.as_view(), name='rest_user_details'),
    path('api/registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('api/login/', LoginView.as_view(), name='rest_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/<str:pk>/', UserViewSetDetail.as_view(), name='user_detail'),
    path('api/user/', UserViewSetList.as_view(), name='user_list'),
    path('api/item/<str:pk>/', ItemViewSetDetail.as_view(), name='item_detail'),
    path('api/item/', ItemViewSetList.as_view(), name='item_list'),
    path('api/categories/', CategoryViewSetList.as_view(), name='category_list'),
    path('api/categories/<str:pk>/', CategoryViewSetDetail.as_view(), name='category_detail'),
    path('api/categoryitems/<str:pk>/', CategoryItemsViewSetDetail.as_view(), name='category_detail'),
    path('api/itemstoexcel/', GenerateItemExcelView.as_view(), name='items_to_excel'),
    path('api/rentalstoexcel/', GenerateRentalExcelView.as_view(), name='rentals_to_excel'),
    path('api/itemcount/', ItemCountView.as_view(), name='item_count'),
    path('api/rentalcount/', RentalCountView.as_view(), name='rental_count'),
    path('api/categoryitemscount/<str:pk>/', CategoryItemsCountView.as_view(), name='category_items_count'),
    path('api/rental/<str:pk>/', RentalViewSetDetail.as_view(), name='rental_detail'),
    path('api/userrentals/', UserRentalViewSetList.as_view(), name='user_rentals'),
    path('api/rental/', RentalViewSetList.as_view(), name='rental_list'),
    path('api/rentitem/', RentItemViewSet.as_view(), name='rent_item'),
    path('api/rental/<str:pk>/approve/', ApproveRentalViewSet.as_view(), name='approve_rental'),
    path('api/rental/<str:pk>/reject/', RejectRentalViewSet.as_view(), name='reject_rental'),
    path('api/rental/<str:pk>/return/', ReturnRentalViewSet.as_view(), name='return_rental'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
