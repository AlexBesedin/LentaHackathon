# Generated by Django 4.2.5 on 2023-09-27 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_sales_import'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales_import',
            name='date',
            field=models.DateField(verbose_name='Дата в файле импорта'),
        ),
    ]
