import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from sales.models import SalesRecord, Sales
from stores.models import Store, StoreID
from categories.models import Category
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Импорт данных о продажах из файла в БД"

    def handle(self, *args, **options):
        with open('data/sales_df_train.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                try:
                    store_id = StoreID.objects.get(title=row[0])
                    store = Store.objects.get(store=store_id)
                    sku = Category.objects.get(sku=row[1])
                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f"Объект не найден: {e}"))
                    continue
                
                date = datetime.strptime(row[2], '%Y-%m-%d').date()
                sales_type = int(row[3])
                sales_units = float(row[4])
                sales_units_promo = float(row[5])
                sales_rub = float(row[6])
                sales_rub_promo = float(row[7])
                
                sales_record, created = SalesRecord.objects.get_or_create(
                    date=date,
                    sales_type=sales_type,
                    sales_units=sales_units,
                    sales_units_promo=sales_units_promo,
                    sales_rub=sales_rub,
                    sales_rub_promo=sales_rub_promo,
                )
                
                sales, created = Sales.objects.get_or_create(
                    store=store,
                    sku=sku,
                    fact=sales_record,
                )
                
                self.stdout.write(self.style.SUCCESS(f"Успешно добавлено/обновлено запись продаж для {store} и {sku} на {date}"))
