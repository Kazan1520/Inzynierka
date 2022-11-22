from abc import ABC
from typing import Type
import pandas as pd
from django.http import FileResponse
from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rest_framework.pagination import LimitOffsetPagination

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

    def get(self, request, format=None):
        self.validate()
        qs = self.model.objects.all()
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserViewSetList(GenericViewSetList):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User


class UserViewSetDetail(GenericViewSetDetail):
    model = User
    serializer_class = UserSerializer


class CategoryViewSetList(GenericViewSetList):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category


class ItemViewSetList(GenericViewSetList):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    model = Item
    paginator = LimitOffsetPagination()


class ItemViewSetDetail(GenericViewSetDetail):
    model = Item
    serializer_class = ItemSerializer


class RentalViewSetList(GenericViewSetList):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    model = Rental


class RentalViewSetDetail(GenericViewSetDetail):
    serializer_class = RentalSerializer
    model = Rental


class SafeConductViewSetList(GenericViewSetList):
    queryset = SafeConduct.objects.all()
    serializer_class = SafeConductSerializer
    model = SafeConduct


class SafeConductViewSetDetail(GenericViewSetDetail):
    serializer_class = SafeConductSerializer
    model = SafeConduct


class MessageViewSetList(GenericViewSetList):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    model = Message


class MessageViewSetDetail(GenericViewSetDetail):
    serializer_class = MessageSerializer
    model = Message


class UserMessagesViewSetList(APIView):

    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryItemsViewSetDetail(APIView):
    paginator = LimitOffsetPagination()

    def get(self, request, pk, format=None):
        items = Item.objects.filter(category=pk)
        qs = self.paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(qs, many=True)
        return Response(serializer.data)


class CategoryItemsCountView(APIView):

    def get(self, request, pk, format=None):
        items = Item.objects.filter(category=pk)
        return Response(items.count())


class ItemRentViewSetList(APIView):

    def get(self, request, pk, format=None):
        rents = Rental.objects.filter(item=pk)
        serializer = ItemRentSerializer(rents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemRentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateItemExcelView(APIView):

    def post(self, request, format=None):
        items = Item.objects.all()
        df = pd.DataFrame(list(items.values()))
        df['created_at'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df['updated_at'] = df['updated_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df.to_excel('items.xlsx', index=False)
        response = Response(status=status.HTTP_200_OK, data={'message': 'Excel file generated'})
        return


class ItemCountView(APIView):

    def get(self, request, format=None):
        items = Item.objects.all()
        return Response(items.count())
