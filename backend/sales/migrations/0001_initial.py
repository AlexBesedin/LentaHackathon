# Generated by Django 4.2.5 on 2023-10-07 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('sales_type', models.IntegerField(verbose_name='Флаг наличия промо')),
                ('sales_units', models.IntegerField(verbose_name='Число проданных товаров без признака промо')),
                ('sales_units_promo', models.IntegerField(verbose_name='Число проданных товаров с признаком промо')),
                ('sales_rub', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Продажи без признака промо в РУБ')),
                ('sales_rub_promo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Продажи с признаком промо в РУБ;')),
            ],
            options={
                'verbose_name': 'Запись продаж',
                'verbose_name_plural': 'Записи продаж',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facts', models.ManyToManyField(related_name='sales_records', to='sales.salesrecord', verbose_name='Записи продаж')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_sales', to='categories.category', verbose_name='Товар')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_sales', to='stores.store', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Продажа',
                'verbose_name_plural': 'Продажи',
            },
        ),
    ]
