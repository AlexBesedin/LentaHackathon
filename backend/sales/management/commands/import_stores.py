import csv


from django.core.management.base import BaseCommand
from stores.models import Store


class Command(BaseCommand):
    help = "Импорт данных магазинов из файла в БД"

    def handle(self, *args, **options):
        with open('data/st_df.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                Store.objects.get_or_create(
                    st_id=row[0],
                    st_city_id=row[1],
                    st_division_code=row[2],
                    st_type_format_id=row[3],
                    st_type_loc_id=row[4],
                    st_type_size_id=row[5],
                    st_is_active=row[6],
                )
