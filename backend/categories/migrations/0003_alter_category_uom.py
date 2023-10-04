from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_category_uom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='uom',


            field=models.IntegerField(choices=[(1, 'Шт.'), (17, 'кг/г')], verbose_name='маркер, обозначающий продаётся товар на вес или в ШТ'),

        ),
    ]
