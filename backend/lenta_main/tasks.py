import requests
from datetime import date, timedelta
from celery import shared_task

from ml.logger_config import _logger
from ml.model import forecast
from ml.constants import URL_FORECAST
from ml.data_services import get_address, get_stores, get_categories, get_sales


@shared_task
def main(today=date.today()):
    _logger.info(f"Запуск основного процесса с указанием даты начала: {today}")
    forecast_dates = [today + timedelta(days=d) for d in range(1, 15)]
    forecast_dates_str = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    
    _logger.info("Получение информации о категориях...")
    categs_info = get_categories()
    
    for store in get_stores():
        _logger.info(f"Обработка магазинов: {store['store']}...")
        result = []

        for item in get_sales(store=store["store"]):
            _logger.debug(f"Обработка товара: {item['sku']} для магазина: {store['store']}...")
            item_info = categs_info.get(item["sku"])
            
            if item_info is None:
                _logger.warning(f"Нет информации о категории для элемента {item['sku']} в магазине {store['store']}")
                continue

            sales = item.get("fact")
            if sales is None:
                _logger.warning(f"Отсутствие данных о продажах для товара {item['sku']}, магазин {store['store']}")
                continue
            
            _logger.debug(f"Прогнозирование для {item['sku']}...")
            prediction = forecast(sales=sales, item_info=item_info, store_info=store)

            result.append({
                "store": store["store"],
                "sku": item["sku"],
                "forecast_date": today.strftime("%Y-%m-%d"),
                "sales_units": [
                    {"date": date, "target": round(target)} for date, target in zip(forecast_dates_str, prediction)
                ]
            })
        if result:
            for r in result:
                _logger.debug(f"Отправка прогноза для магазина: {store['store']}, SKU {r['sku']} to the API...")
                response = requests.post(get_address(URL_FORECAST), json=r, headers={'Content-Type': 'application/json'})
                
                if response.status_code == 201:
                    _logger.info("Данные успешно отправлены!")
                else:
                    _logger.error(f"Не удалось отправить данные! Код состояния: {response.status_code}, Response text: {response.text}")
        else:
            _logger.warning(f"Нет данных для передачи в магазин {store['store']}")

if __name__ == "__main__":
    main.delay()