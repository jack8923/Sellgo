from django.contrib import admin

# Register your models here.
from .models import csv_product, customer

admin.site.register(csv_product)
admin.site.register(customer)