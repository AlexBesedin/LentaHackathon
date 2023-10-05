# Generated by Django 4.2.5 on 2023-10-05 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('stores', '0001_initial'),
        ('forecast', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='storeforecast',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_forecasts', to='categories.category', verbose_name='захэшированное id товара'),
        ),
        migrations.AddField(
            model_name='storeforecast',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='stores.store', verbose_name='захэшированное id магазина'),
        ),
        migrations.AddField(
            model_name='dailysalesforecast',
            name='forecast_sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_units', to='forecast.storeforecast', verbose_name='Прогноз товара'),
        ),
        migrations.AlterUniqueTogether(
            name='userbookmark',
            unique_together={('user', 'store_forecast')},
        ),
    ]