# Generated by Django 5.0.2 on 2024-05-16 15:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name=datetime.datetime(2024, 5, 16, 17, 34, 51, 389565)),
        ),
    ]
