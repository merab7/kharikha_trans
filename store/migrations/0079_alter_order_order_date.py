# Generated by Django 5.0.4 on 2024-07-29 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0078_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name=datetime.datetime(2024, 7, 29, 12, 12, 38, 971851)),
        ),
    ]
