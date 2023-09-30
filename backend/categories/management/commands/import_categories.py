import csv

from categories.models import Category, CategoryProduct, Group, Subcategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Импорт данных продуктовых категорий из файла в БД"

    def handle(self, *args, **options):
        with open('data/pr_df.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                group, _ = Group.objects.get_or_create(group=row[1])
                category_product, _ = CategoryProduct.objects.get_or_create(
                    category=row[2],
                    group=group,
                )
                subcategory, _ = Subcategory.objects.get_or_create(
                    subcategory=row[3],
                    category=category_product,
                )

                Category.objects.get_or_create(
                    sku=row[0],
                    group=group,
                    category=category_product,
                    subcategory=subcategory,
                    uom=row[4],
                )
