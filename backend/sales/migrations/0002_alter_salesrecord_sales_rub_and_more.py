# Generated by Django 4.2.5 on 2023-09-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesrecord',
            name='sales_rub',
            field=models.DecimalField(choices=[('rub', 'Рубли')], decimal_places=2, max_digits=10, verbose_name='продажи без признака промо в РУБ'),
        ),
        migrations.AlterField(
            model_name='salesrecord',
            name='sales_run_promo',
            field=models.DecimalField(choices=[('rub', 'Рубли')], decimal_places=2, max_digits=10, verbose_name='продажи с признаком промо в РУБ;'),
        ),
    ]
