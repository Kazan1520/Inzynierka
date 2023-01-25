import datetime
import pandas as pd
from django.http import HttpResponse
from dj_rest_auth.registration.views import RegisterView
from django_filters.rest_framework import filters, DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rental_service.permissions import IsAdminOrReadOnly, IsUserOwner
from rental_service.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rental_service.serializers import *
from rest_framework import status


class GenericViewSetMixin:
    queryset = None
    serializer_class = None
    model = None
    save_serializer_class = None
    paginator = None

    def validate(self):
        assert (self.model != None), f'Model not defined in {self.__class__.__name__}'
        assert (self.serializer_class != None), f'Serializer_class not defined in {self.__class__.__name__}'

    def check_model(self, raise_error=True):
        for attr in self.__dict__:
            print(attr)
            if attr == "save_serializer_class":
                return
            if attr is None:
                if raise_error:
                    raise TypeError
                else:
                    print(f'There\'s a problem with class {self.__name__}')


class GenericViewSetList(APIView, GenericViewSetMixin):

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, format=None):
        self.validate()
        qs = self.get_queryset()
        count = qs.count()
        if self.paginator:
            qs = self.paginator.paginate_queryset(qs, request)

        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.save_serializer_class(data=request.data) if self.save_serializer_class \
            else self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenericViewSetDetail(APIView, GenericViewSetMixin):

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = self.serializer_class(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = self.save_serializer_class(qs, data=request.data) if self.save_serializer_class else \
            self.serializer_class(qs, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        qs = self.get_object(pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = self.save_serializer_class(qs, data=request.data, partial=True) if self.save_serializer_class \
            else self.serializer_class(qs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserViewSetList(GenericViewSetList):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User
    permission_classes = [IsAdminUser]


class UserViewSetDetail(GenericViewSetDetail):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsUserOwner, IsAdminUser]


class CategoryViewSetList(GenericViewSetList):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category
    permission_classes = [IsAdminOrReadOnly]


class ItemViewSetList(GenericViewSetList):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    model = Item
    paginator = LimitOffsetPagination()
    permission_classes = [IsAdminOrReadOnly]

    def search_items(self, search_term):
        return self.queryset.filter(
            Q(id__icontains=search_term) |
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(serial_number__icontains=search_term)
        )

    def get_queryset(self):
        queryset = self.queryset
        search_term = self.request.query_params.get('q')
        if search_term:
            queryset = self.search_items(search_term)
        return queryset

    def post(self, request, format=None):
        serializer = ItemSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemViewSetDetail(GenericViewSetDetail):
    model = Item
    serializer_class = ItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = ItemSaveSerializer(qs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSetDetail(GenericViewSetDetail):
    model = Category
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class RentalViewSetList(GenericViewSetList):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    model = Rental
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset.order_by('-updated_at')
        search_term = self.request.query_params.get('q')
        if search_term:
            queryset = self.search_rentals(search_term)
        return queryset

    def search_rentals(self, search_term):
        return self.queryset.filter(
            Q(id__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(item__description__icontains=search_term) |
            Q(item__serial_number__icontains=search_term)
        )


class RentalViewSetDetail(GenericViewSetDetail):
    serializer_class = RentalSerializer
    model = Rental
    permission_classes = [IsAdminOrReadOnly]


class CategoryItemsViewSetDetail(APIView):
    paginator = LimitOffsetPagination()
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk, format=None):
        items = Item.objects.filter(category=pk)
        qs = self.paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(qs, many=True)
        return Response(serializer.data)


class CategoryItemsCountView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk, format=None):
        items = Item.objects.filter(category=pk).order_by('-updated_at')
        return Response(items.count())


class GenerateItemExcelView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        items = Item.objects.all()
        df = pd.DataFrame(list(items.values()))
        df['created_at'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df['updated_at'] = df['updated_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        date = datetime.datetime.now().strftime('%Y%m%d%H%M')
        df.to_excel(f'pliki\\{date}.xlsx', index=False)
        response = HttpResponse(open(f'pliki\\{date}.xlsx', 'rb'), status=status.HTTP_200_OK, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="%s"' % f'{date}.xlsx'
        return response


class GenerateRentalExcelView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        rentals = Rental.objects.all()
        df = pd.DataFrame(list(rentals.values()))
        df['created_at'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df['updated_at'] = df['updated_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        date = datetime.datetime.now().strftime('%Y%m%d%H%M')
        df.to_excel(f'pliki\\{date}.xlsx', index=False)
        response = HttpResponse(open(f'pliki\\{date}.xlsx', 'rb'), status=status.HTTP_200_OK, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="%s"' % f'{date}.xlsx'
        return response


class ItemCountView(APIView):
    queryset = Item.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def search_items(self, search_term):
        return self.queryset.filter(
            Q(id__icontains=search_term) |
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(serial_number__icontains=search_term)
        )

    def get_queryset(self):
        queryset = self.queryset
        search_term = self.request.query_params.get('q')
        if search_term:
            queryset = self.search_items(search_term)
        return queryset

    def get(self, request, format=None):
        items = self.get_queryset()
        return Response(items.count())


class RentalCountView(APIView):
    queryset = Rental.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        search_term = self.request.query_params.get('q')
        if search_term:
            queryset = self.search_rentals(search_term)
        return queryset

    def get(self, request, format=None):
        rentals = self.get_queryset()
        return Response(rentals.count())

    def search_rentals(self, search_term):
        return self.queryset.filter(
            Q(id__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(item__description__icontains=search_term) |
            Q(item__serial_number__icontains=search_term)
        )


class UserRentalViewSetList(APIView):
    permission_classes = [IsUserOwner, IsAdminUser]

    def get(self, request, format=None):
        rents = Rental.objects.filter(user=self.request.user)
        serializer = RentalSerializer(rents, many=True)
        return Response(serializer.data)


class ApproveRentalViewSet(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk, format=None):
        rental = Rental.objects.get(id=pk)
        rental.status = "Not returned"
        rental.save()
        return Response(status=status.HTTP_200_OK)


class RejectRentalViewSet(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk, format=None):
        rental = Rental.objects.get(id=pk)
        rental.status = "Rejected"
        rental.item.status = "Available"
        rental.save()
        rental.item.save()
        return Response(status=status.HTTP_200_OK)


class ReturnRentalViewSet(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk, format=None):
        rental = Rental.objects.get(id=pk)
        rental.status = "Returned"
        rental.item.status = "Available"
        rental.save()
        rental.item.save()
        return Response(status=status.HTTP_200_OK)


class RentItemViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        item = Item.objects.get(id=request.data.get('item'))
        if item.status == "Available":
            item.status = "Rented"
            item.save()
            serializer = RentalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(item=item, user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
