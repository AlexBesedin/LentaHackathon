from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='захэшированное id города')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('city',),
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=50, verbose_name='захэшированное id дивизиона')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
                'ordering': ('division',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc', models.IntegerField(verbose_name='id тип локации/окружения магазина')),
            ],
            options={
                'verbose_name': 'Тип локации магазины',
                'verbose_name_plural': 'Типы локаций магазинов',
                'ordering': ('loc',),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(verbose_name='id типа размера магазина')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
                'ordering': ('size',),
            },
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(max_length=50, verbose_name='захэшированное id магазина')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ('store',),
            },
        ),
        migrations.CreateModel(
            name='Type_format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_format', models.IntegerField(verbose_name='id формата магазина')),
            ],
            options={
                'verbose_name': 'Формат магазины',
                'verbose_name_plural': 'Форматы магазинов',
                'ordering': ('type_format',),
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(verbose_name='id типа размера магазина')),
                ('is_active', models.BooleanField(verbose_name='флаг активного магазина на данный момент')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='stores.city')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='stores.division')),
                ('loc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locs', to='stores.location')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='stores.stores')),
                ('type_format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_formats', to='stores.type_format')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ('store',),
            },
        ),
    ]
