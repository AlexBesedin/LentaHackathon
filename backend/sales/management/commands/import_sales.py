import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from sales.models import Sales, SalesRecord
from stores.models import Store, Stores
from categories.models import Category

class Command(BaseCommand):
    help = "Импорт данных продаж из файла в БД"

    def handle(self, *args, **options):
        with open('data/sales_df_train.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)  
            for row in file_reader:
                store, _ = Stores.objects.get_or_create(store=row[0])
                store_instance, _ = Store.objects.get_or_create(store=store) 
                sku, _ = Category.objects.get_or_create(sku=row[1]) 

                sales, _ = Sales.objects.get_or_create(store=store_instance, sku=sku)
                
                date = datetime.strptime(row[2], '%Y-%m-%d').date()
                sales_type = int(row[3])
                sales_units = float(row[4])
                sales_units_promo = float(row[5])
                sales_rub = float(row[6])
                sales_rub_promo = float(row[7])
                
                SalesRecord.objects.get_or_create(
                    fact=sales,
                    date=date,
                    sales_type=sales_type,
                    sales_units=sales_units,
                    sales_units_promo=sales_units_promo,
                    sales_rub=sales_rub,
                    sales_rub_promo=sales_rub_promo,
                )

                