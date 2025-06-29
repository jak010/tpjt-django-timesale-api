# Generated by Django 5.2.3 on 2025-06-19 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.BigIntegerField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'products',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TimeSale',
            fields=[
                ('timesale_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.BigIntegerField()),
                ('remaining_quantity', models.BigIntegerField()),
                ('discount_price', models.BigIntegerField()),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20)),
                ('version', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sales', to='apps.product')),
            ],
            options={
                'db_table': 'time_sales',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TimeSaleOrder',
            fields=[
                ('timesale_order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField()),
                ('quantity', models.BigIntegerField()),
                ('discount_price', models.BigIntegerField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='apps.timesale')),
            ],
            options={
                'db_table': 'time_sale_orders',
            },
        ),
    ]
