from django.shortcuts import render
import logging
from .models import customer, csv_product
from .serializers import ProductSerializer, CustomerSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from distutils.util import strtobool
from .errors import CustomValidationError
from django.contrib import messages
import csv
from rest_framework.decorators import api_view
from django.http import HttpResponse
import pandas as pd

logger = logging.getLogger(__name__)


class CustomerList(APIView):
    """
    List all Customers, or create a new snippet.
    """
    def get(self, request, format=None):
        users = customer.objects.all()
        serializer = CustomerSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def CustomerDetail(request, pk):
    users = csv_product.objects.raw('select distinct customer.id as customer_id,customer.name as customer_name,csv_product.title as product_title,csv_product.price as product_price,csv_product.id as id,csv_product.uploaded_date as last_uploaded from customer as customer inner join csv_product as csv_product on customer.id = csv_product.customer_id where customer.id = %s and uploaded_date in (select max(uploaded_date) from csv_product group by customer_id,title);', [pk])
    serializer = ProductSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def ProductList(request):
    """
    List all Products, or create a new snippet.
    """
    template = "upload.html"
    products = csv_product.objects.all()

    prompt = {
        'order': 'Order of the CSV should be Title, Price',
        'profiles': products
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    customer_id = request.POST["customer_id"]

    csv_file = request.FILES['file']
    user = customer.objects.get(pk=customer_id)
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
        return HttpResponse(status=500)

    if user is None:
        messages.error(request, 'Invalid customer_id')
        return HttpResponse(status=500)


    city_data = pd.read_csv(csv_file, encoding= 'unicode_escape')
    print("Data Shape", city_data.shape)
    for index, row in city_data.iterrows():

        # curr_product, is_created = csv_product.objects.get_or_create(
        #     title=str(row['Title']), price=float(row['Price']), customer_id=customer_id)
        # print("Product added ")

        try:
            curr_product, is_created = csv_product.objects.get_or_create(
                title=str(row['Title']), price=float(row['Price']),customer_id=customer_id)
            print("Product added ")
        except:
            print("product with title " + str(row['Title']) + " not added")

    messages.error(request, 'Products Added')
    return HttpResponse(status=200)