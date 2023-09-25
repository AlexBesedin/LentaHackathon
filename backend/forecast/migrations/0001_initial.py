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
            name='StoreForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateField(verbose_name='Дата прогноза')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='stores.store', verbose_name='захэшированное id магазина')),
            ],
            options={
                'verbose_name': 'Прогноз магазина',
                'verbose_name_plural': 'Прогнозы магазинов',
            },
        ),
        migrations.CreateModel(
            name='SkuForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_forecasts', to='forecast.storeforecast', verbose_name='Прогноз магазина')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_forecasts', to='categories.category', verbose_name='захэшированное id товара')),
            ],
            options={
                'verbose_name': 'Прогноз товара',
                'verbose_name_plural': 'Прогнозы товаров',
            },
        ),
        migrations.CreateModel(
            name='DailySalesForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата(день)')),
                ('target', models.PositiveIntegerField(verbose_name='спрос в ШТ.')),
                ('sales_units', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.skuforecast', verbose_name='Прогноз товара')),
            ],
            options={
                'verbose_name': 'Ежедневный прогноз продаж',
                'verbose_name_plural': 'Ежедневные прогнозы продаж',
            },
        ),
    ]
