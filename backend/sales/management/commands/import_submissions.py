import csv

from categories.models import Category
from django.core.management.base import BaseCommand
from forecast.models import DailySalesForecast
from stores.models import Stores


class Command(BaseCommand):
    help = "Импорт данных магазинов из файла в БД"

    def handle(self, *args, **options):
        with open('data/sales_submission.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                Stores.objects.get_or_create(
                    store=row[0],
                )
                Category.objects.get_or_create(
                    sku=row[0],
                )
                DailySalesForecast.get_or_create(
                    date=row[2],
                    target=row[3],
                )
