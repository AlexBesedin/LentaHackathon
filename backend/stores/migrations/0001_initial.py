# Generated by Django 4.2.5 on 2023-09-29 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='захэшированное id магазина')),
            ],
            options={
                'verbose_name': 'ID магазина',
                'verbose_name_plural': 'ID магазинов',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='захэшированное id города')),
                ('division', models.CharField(max_length=50, verbose_name='захэшированное id дивизиона')),
                ('type_format', models.IntegerField(verbose_name='id формата магазина')),
                ('loc', models.IntegerField(verbose_name='id тип локации/окружения магазина')),
                ('size', models.IntegerField(null=True, verbose_name='id типа размера магазина')),
                ('is_active', models.BooleanField(verbose_name='флаг активного магазина на данный момент')),
                ('store', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='stores.storeid', verbose_name='захэшированное id магазина')),
            ],
            options={
                'verbose_name': 'Сводная таблица магазина',
                'verbose_name_plural': 'Сводная таблица магазинов',
                'ordering': ('store',),
            },
        ),
    ]
