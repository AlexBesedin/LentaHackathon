import csv

from django.core.management.base import BaseCommand
from stores.models import Store


class Command(BaseCommand):
    help = "Импорт данных магазинов из файла в БД"

    def handle(self, *args, **options):
        with open('data/st_df.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                Store.objects.get_or_create(
                    store=row[0],
                    city=row[1],
                    division=row[2],
                    type_format=row[3],
                    loc=row[4],
                    size=row[5],
                    is_active=bool(row[6]),
                )
