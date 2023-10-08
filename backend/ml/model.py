from datetime import date, timedelta

import joblib
import pandas as pd
from joblib import Parallel, delayed
from prophet import Prophet


def forecast(sales: dict, item_info: dict, store_info: dict) -> list:
    """
    Функция для предсказания продаж
    :params sales: исторические данные по продажам
    :params item_info: характеристики товара
    :params store_info: характеристики магазина

    """
    sales = pd.DataFrame([sales])
    item_info = pd.DataFrame([item_info])
    store_info = pd.DataFrame([store_info])

    a = store_info['store'].values[0]
    b = item_info['sku'].values[0]
    c = sales['sales_type']
    sales['store'] = a
    sales['sku'] = b

    forecast_dates = [date.today() + timedelta(days=d) for d in range(1, 14)]
    forecast_dates = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    forecast_dates = pd.DataFrame(forecast_dates, columns=['date'])
    forecast_dates['st_id'] = a
    forecast_dates['pr_sku_id'] = b
    forecast_dates['pr_sales_type_id'] = c
    #Правки
    forecast_dates['date'] = pd.to_datetime(forecast_dates['date'])
    forecast_dates['dayofweek'] = forecast_dates['date'].dt.dayofweek


    forecast_dates = pd.merge(forecast_dates, item_info, on='sku')
    forecast_dates = pd.merge(forecast_dates, store_info, on='store')

    sales = pd.merge(sales, item_info, on='sku')
    sales = pd.merge(sales, store_info, on='store')

    sales.rename(columns={'sku' : 'pr_sku_id',
                          'store' : 'st_id',
                          'date' : 'date',
                          'city' : 'st_city_id',
                          'division' : 'st_division_id',
                          'type_format' : 'st_type_format_id',
                          'loc' : 'st_type_loc_id',
                          'size' : 'st_type_size_id',
                          'is_active' : 'st_is_active',
                          'group' : 'pr_group_id',
                          'category' : 'pr_cat_id',
                          'subcategory' : 'pr_subcat_id',
                          'uom' : 'pr_uom_id',
                          'sales_type' : 'pr_sales_type_id',
                          'sales_units' : 'pr_sales_in_units',
                          'sales_units_promo' : 'pr_promo_sales_in_units',
                          'sales_rub': 'pr_sales_in_rub',
                          'sales_rub_promo': 'pr_promo_sales_in_rub',
                          'dayofweek': 'dayofweek'
                          }, inplace=True)

    forecast_dates.rename(columns={'pr_sku_id': 'pr_sku_id',
                          'st_id': 'st_id',
                          'date': 'date',
                          'city': 'st_city_id',
                          'division': 'st_division_id',
                          'type_format': 'st_type_format_id',
                          'loc': 'st_type_loc_id',
                          'size': 'st_type_size_id',
                          'is_active': 'st_is_active',
                          'group': 'pr_group_id',
                          'category': 'pr_cat_id',
                          'subcategory': 'pr_subcat_id',
                          'uom': 'pr_uom_id',
                          'pr_sales_type_id': 'pr_sales_type_id'

                          }, inplace=True)

    product_labels = pd.read_csv('ml/products_labels.csv')
    product_labels = product_labels[['product_clasters', 'pr_sku_id']]
    forecast_dates = pd.merge(forecast_dates, product_labels, on="pr_sku_id")

    price_labels = pd.read_csv('ml/price_labels.csv')
    price_labels = price_labels[['price_clasters', 'pr_sku_id']]
    forecast_dates = pd.merge(forecast_dates, price_labels, on="pr_sku_id")

    prophet_m = joblib.load('ml/prophet_m.pkl')
    future = prophet_m.make_future_dataframe(periods=14, freq='D')
    forecast = prophet_m.predict(future)
    forecast['date'] = forecast['ds']
    forecast = forecast[['trend', 'date', 'trend_upper', 'trend_lower', 'yhat']]
    forecast_dates = pd.merge(forecast_dates, forecast, on='date')

    holidays_df = pd.read_csv('ml/holidays_covid_calendar.csv')
    list_col = ['date', 'holiday']
    forecast_dates = forecast_dates.merge(holidays_df[list_col], on="date", how='inner')
    forecast_dates = forecast_dates.drop('st_is_active', axis=1)
    date_1 = -1
    rol7, rol14, pr_sales_median, pr_sales_max, pr_sales_min, pr_sales_var = [], [], [], [], [], []
    lag_7, lag_14, lag_1, lag_2, lag_3, lag_4, lag_5, lag_6, lag_8, lag_9, lag_10, lag_11, lag_12, lag_13 =\
        [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for i in range(1, 15):
        a = sales['date'].iloc[date_1 - 15:date_1]
        b = sales[sales['date'].isin(a)]['pr_sales_in_units']
        rol = b.shift().rolling(window=7).mean()
        rol = rol.iloc[-1]
        rol7.append(b)

        rol = b.shift().rolling(window=14).mean()
        rol = rol.iloc[-1]
        rol14.append(b)

        rol = b.shift().rolling(window=14).min()
        rol = rol.iloc[-1]
        pr_sales_min.append(b)

        rol = b.shift().rolling(window=14).max()
        rol = rol.iloc[-1]
        pr_sales_max.append(b)

        rol = b.shift().rolling(window=14).median()
        rol = rol.iloc[-1]
        pr_sales_median.append(b)

        rol = b.shift().rolling(window=14).var()
        rol = rol.iloc[-1]
        pr_sales_var.append(b)

        lag_1.append(b.iloc[-2])
        lag_2.append(b.iloc[-3])
        lag_3.append(b.iloc[-4])
        lag_4.append(b.iloc[-5])
        lag_5.append(b.iloc[-6])
        lag_6.append(b.iloc[-7])
        lag_7.append(b.iloc[-8])
        lag_8.append(b.iloc[-9])
        lag_9.append(b.iloc[-10])
        lag_10.append(b.iloc[-11])
        lag_11.append(b.iloc[-12])
        lag_12.append(b.iloc[-13])
        lag_13.append(b.iloc[-14])
        lag_14.append(b.iloc[-15])

        date_1 -= 1

    forecast_dates['rol7'] = rol7
    forecast_dates['rol14'] = rol14
    forecast_dates['pr_sales_min'] = pr_sales_min
    forecast_dates['pr_sales_max'] = pr_sales_max
    forecast_dates['pr_sales_median'] = pr_sales_median
    forecast_dates['pr_sales_variance'] = pr_sales_var
    forecast_dates['lag_1'] = lag_1
    forecast_dates['lag_2'] = lag_2
    forecast_dates['lag_3'] = lag_3
    forecast_dates['lag_4'] = lag_4
    forecast_dates['lag_5'] = lag_5
    forecast_dates['lag_6'] = lag_6
    forecast_dates['lag_7'] = lag_7
    forecast_dates['lag_8'] = lag_8
    forecast_dates['lag_9'] = lag_9
    forecast_dates['lag_10'] = lag_10
    forecast_dates['lag_11'] = lag_11
    forecast_dates['lag_12'] = lag_12
    forecast_dates['lag_13'] = lag_13
    forecast_dates['lag_14'] = lag_14

    model = joblib.load('ml/catboost.plk')
    predictions = model.predict(forecast_dates)

    return predictions


