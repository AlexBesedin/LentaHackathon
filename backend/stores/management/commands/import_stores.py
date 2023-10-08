import csv

from django.core.management.base import BaseCommand

from stores.models import Store, StoreID


class Command(BaseCommand):
    help = "Импорт данных магазинов из файла в БД"

    def handle(self, *args, **options):
        with open('data/st_df.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                store_id, created = StoreID.objects.get_or_create(title=row[0])
                if store_id:
                    Store.objects.update_or_create(
                        store=store_id,
                        defaults={
                            'city': row[1],
                            'division': row[2],
                            'type_format': int(row[3]),
                            'loc': int(row[4]),
                            'size': int(row[5]),
                            'is_active': bool(row[6]),
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"Успешно добавлено/обновлено магазин {store_id.title}"
                        )
                    )
