import csv

from categories.models import Category
from django.core.management.base import BaseCommand
from sales.models import SalesRecord
from stores.models import Store


class Command(BaseCommand):
    help = "Импорт данных о продажах из файла в БД"

    def handle(self, *args, **options):
        with open('data/sales_df_train.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                SalesRecord.objects.get_or_create(
                    date=row[2],
                    sales_type=int(row[3]),
                    sales_units=float(row[4]),
                    sales_units_promo=float(row[5]),
                    sales_rub=float(row[6]),
                    sales_run_promo=float(row[7]),
                ),
                Category.objects.get_or_create(
                    sku=row[1],
                ),
                Store.objects.get_or_create(store=row[0],)
