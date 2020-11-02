# Generated by Django 2.1.5 on 2020-10-31 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20201031_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csv_product',
            name='my_float',
        ),
        migrations.AlterField(
            model_name='csv_product',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.customer'),
        ),
    ]