from rest_framework import serializers
from .models import customer, csv_product
from django.db import transaction
from django.db.utils import IntegrityError
from .behaviours import DynamicFieldsMixin


class ProductSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = csv_product
        fields = ('customer_id', 'customer_name', 'title', 'price', 'id', 'uploaded_date')

    def create(self, validated_data):
        try:
            with transaction.atomic():
                c_id = validated_data.get('customer_id')
                if c_id is not None:
                    product = csv_product.objects.create(title=validated_data.get('title'),
                                                         price=validated_data.get('price'),
                                                         customer_id=c_id)
                else:
                    product = csv_product.objects.create(title=validated_data.get('title'),
                                                         price=validated_data.get('price'))

        except IntegrityError:
            print('Integrity Error')

        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)

        initial_value = self.initial_data

        instance.save()
        return instance

    def validate(self, data):
        # print('validate mein ghus gaya')
        # ArticleHelper.cneck_title_unique(data)
        validated_data = super().validate(data)
        return validated_data


class CustomerSerializer(DynamicFieldsMixin,serializers.ModelSerializer):

    class Meta:
        model = customer
        fields = ('id', 'name', 'email', 'created_date')

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = customer.objects.create(name=validated_data.get('name'), email=validated_data.get('email'))
        except IntegrityError:
            print('Integrity Error')

        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)

        initial_value = self.initial_data

        instance.save()
        return instance

    def validate(self, data):
        # print('validate mein ghus gaya')
        # ArticleHelper.cneck_title_unique(data)
        validated_data = super().validate(data)
        return validated_data
