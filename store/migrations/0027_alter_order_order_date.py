# Generated by Django 5.0.4 on 2024-05-03 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_remove_product_quantity_remove_product_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name=datetime.datetime(2024, 5, 3, 18, 58, 21, 634115)),
        ),
    ]
