import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from forecast.models import StoreForecast, DailySalesForecast
from stores.models import Store
from categories.models import Category
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Импорт данных прогнозов из файла в БД"

    def handle(self, *args, **options):
        with open('data/sales_submission.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                try:
                    store = Store.objects.get(store=row[0])
                    sku = Category.objects.get(sku=row[1])
                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f"Объект не найден: {e}"))
                    continue
                forecast_date = datetime.strptime(row[2], '%Y-%m-%d').date()
                target = int(row[3])
                store_forecast, created = StoreForecast.objects.get_or_create(
                    store=store,
                    sku=sku,
                    forecast_date=forecast_date,
                )
                DailySalesForecast.objects.update_or_create(
                    forecast_sku_id=store_forecast,
                    date=forecast_date,
                    defaults={'target': target},
                )
                self.stdout.write(self.style.SUCCESS(f"Успешно добавлено/обновлено прогноз для {store} и {sku} на {forecast_date}"))

