import csv

from celery import current_task
from django.core.management.base import BaseCommand
from stores.models import Category


class Command(BaseCommand):
    help = "Импорт данных продуктовых категорий из файла в БД"

    def handle(self, *args, **options):
        with open('data/pr_df.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            total_rows = sum(1 for row in file_reader)
        
        with open('data/pr_df.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for i, row in enumerate(file_reader, 1):
                Category.objects.get_or_create(
                    pr_sku_id=row[0],
                    pr_group_id=row[1],
                    pr_cat_id=row[3],
                    pr_subcat_id=row[4],
                    pr_uom_id=row[5],
                )
                current_task.update_state(
                    state='PROGRESS',
                    meta={'current': i, 'total': total_rows}
                )
