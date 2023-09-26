# Generated by Django 4.2.5 on 2023-09-26 10:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_sales', to='categories.category', verbose_name='захэшированное id товара')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_sales', to='stores.store', verbose_name='захэшированное id магазина')),
            ],
            options={
                'verbose_name': 'Продажа',
                'verbose_name_plural': 'Продажи',
            },
        ),
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('sales_type', models.IntegerField(verbose_name='флаг наличия промо')),
                ('sales_units', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='число проданных товаров без признака промо')),
                ('sales_units_promo', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='число проданных товаров с признаком промо')),
                ('sales_rub', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='продажи без признака промо в РУБ')),
                ('sales_rub_promo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='продажи с признаком промо в РУБ;')),
                ('fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_records', to='sales.sales')),
            ],
            options={
                'verbose_name': 'Запись продаж',
                'verbose_name_plural': 'Записи продаж',
            },
        ),
    ]