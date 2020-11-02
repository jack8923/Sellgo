# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.


class customer(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Customer Name"
    )

    email = models.EmailField(
        max_length=254,
        verbose_name="email"
    )

    created_date = models.DateTimeField(
        default=datetime.now,
        verbose_name="created_at"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "customer"
        verbose_name = "Customer"


class csv_product(models.Model):
    customer = models.ForeignKey(
        customer,
        on_delete=models.CASCADE,
        related_name='products'
    )

    title = models.CharField(
        max_length=500,
        verbose_name='Product Title'
    )

    price = models.FloatField(
    )

    uploaded_date = models.DateTimeField(
        default=datetime.now,
        verbose_name="uploaded_date"
    )

    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super(csv_product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "csv_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"