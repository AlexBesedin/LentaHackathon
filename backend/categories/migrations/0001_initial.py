from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, verbose_name='захэшированная категория товара')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('category',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=50, verbose_name='захэшированная группа товара')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ('group',),
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(max_length=50, verbose_name='захэшированная подкатегория товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='categories.categoryproduct')),
            ],
            options={
                'verbose_name': 'Субкатегория',
                'verbose_name_plural': 'Субкатегории',
            },
        ),
        migrations.AddField(
            model_name='categoryproduct',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='categories.group'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=50, verbose_name='захэшированное id товара')),
                ('uom', models.PositiveIntegerField(verbose_name='маркер, обозначающий продаётся товар на вес или в ШТ')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_categories', to='categories.categoryproduct')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_groups', to='categories.group')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_subcategories', to='categories.subcategory')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('group', 'category', 'subcategory', 'sku'),
            },
        ),
    ]
