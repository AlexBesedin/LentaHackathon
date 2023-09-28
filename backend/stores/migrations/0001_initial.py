from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(max_length=50, verbose_name='захэшированное id магазина')),
                ('city', models.CharField(max_length=50, verbose_name='захэшированное id города')),
                ('division', models.CharField(max_length=50, verbose_name='захэшированное id дивизиона')),
                ('type_format', models.IntegerField(verbose_name='id формата магазина')),
                ('loc', models.IntegerField(verbose_name='id тип локации/окружения магазина')),
                ('size', models.IntegerField(null=True, verbose_name='id типа размера магазина')),
                ('is_active', models.BooleanField(verbose_name='флаг активного магазина на данный момент')),
            ],
            options={
                'verbose_name': 'Сводная таблица магазина',
                'verbose_name_plural': 'Сводная таблица магазинов',
                'ordering': ('store',),
            },
        ),
    ]
