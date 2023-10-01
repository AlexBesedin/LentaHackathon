from datetime import date, timedelta
import requests

from data_services import fetch_data, get_address
from constants import URL_CATEGORIES, URL_SALES, URL_STORES, URL_FORECAST
from model import forecast
from logger_config import logger


def main(today=date.today()):
    forecast_dates = [today + timedelta(days=d) for d in range(1, 6)]
    forecast_dates = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    categs_info = fetch_data(get_address(URL_CATEGORIES))
    if not categs_info:
        logger.warning("Не удалось получить информацию о категории")
    stores = fetch_data(get_address(URL_STORES))
    if not stores:
        logger.warning("Не удалось получить данные о магазинах")
    for store in stores:
        result = []
        sales = fetch_data(get_address(URL_SALES), params={"store": store["store"]})
        if not sales:
            logger.warning(f"Не удалось получить данные о продажах для магазина {store['store']}")
        for item in sales:
            item_info = categs_info.get(item["sku"])
            if item_info:
                sales_data = item["fact"]
                prediction = forecast(sales_data, item_info, store)
                result.append({
                    "store": store["store"],
                    "forecast_date": today.strftime("%Y-%m-%d"),
                    "forecast": {
                        "sku": item["sku"],
                        "sales_units": dict(zip(forecast_dates, prediction))
                    }
                })
        response = requests.post(get_address(URL_FORECAST), json={"data": result})
        if response.status_code != 200:
            logger.error(f"Не удалось опубликовать данные прогноза для магазина {store['store']}. Status code: {response.status_code}")


if __name__ == "__main__":
    logger.info("Запуск обработки прогноза")
    main()
    logger.info("Обработка готовых прогнозов")

