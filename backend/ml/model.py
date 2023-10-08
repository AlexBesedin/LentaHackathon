import pandas as pd
import joblib
from datetime import date, timedelta
from prophet import Prophet
from joblib import Parallel, delayed

def forecast(sales: dict, item_info: dict, store_info: dict) -> list:
    """
    Функция для предсказания продаж
    :params sales: исторические данные по продажам
    :params item_info: характеристики товара
    :params store_info: характеристики магазина

    """
    sales = pd.DataFrame(sales)
    item_info = pd.DataFrame(item_info, index = [0])
    store_info = pd.DataFrame(store_info, index = [0])

    a = store_info['store'].values[0]
    b = item_info['sku'].values[0]
    c = sales['sales_type'].values[0]
    sales['store'] = a
    sales['sku'] = b

    forecast_dates = [date.today() + timedelta(days=d) for d in range(1, 15)]
    forecast_dates = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    forecast_dates = pd.DataFrame(forecast_dates, columns=['date'])
    forecast_dates['store'] = a
    forecast_dates['sku'] = b
    forecast_dates['pr_sales_type_id'] = int(c)
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

    forecast_dates.rename(columns={'sku': 'pr_sku_id',
                          'store': 'st_id',
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

    product_labels = pd.read_csv('ml/data_ml/products_labels.csv')
    product_labels = product_labels[['product_clasters', 'pr_sku_id']]
    forecast_dates = pd.merge(forecast_dates, product_labels, on="pr_sku_id")

    price_labels = pd.read_csv('ml/data_ml/price_labels.csv')
    price_labels = price_labels[['price_clasters', 'pr_sku_id']]
    forecast_dates = pd.merge(forecast_dates, price_labels, on="pr_sku_id")
    prophet_m = joblib.load('ml/data_ml/proph.pkl')
    future = prophet_m.make_future_dataframe(periods=100, freq='D')
    forecast = prophet_m.predict(future)
    forecast['date'] = forecast['ds']
    forecast = forecast[['trend', 'date', 'trend_upper', 'trend_lower', 'yhat']]
    forecast_dates = pd.merge(forecast_dates, forecast, on='date')
    holidays_df = pd.read_csv('ml/data_ml/holidays_covid_calendar.csv')
    list_col = ['date', 'holiday']
    holidays_df['date'] = pd.to_datetime(holidays_df['date'], format = '%d.%m.%Y')
    forecast_dates = forecast_dates.merge(holidays_df[list_col], on="date", how='inner')
    forecast_dates = forecast_dates.drop('st_is_active', axis=1)

    units = sales['pr_sales_in_units']

    forecast_dates['rol7'] = 0
    forecast_dates['rol14'] = 0
    forecast_dates['pr_sales_min'] = 0
    forecast_dates['pr_sales_max'] = 0
    forecast_dates['pr_sales_median'] = 0
    forecast_dates['pr_sales_variance'] = 0
    forecast_dates['lag_1'] = 0
    forecast_dates['lag_2'] = 0
    forecast_dates['lag_3'] = 0
    forecast_dates['lag_4'] = 0
    forecast_dates['lag_5'] = 0
    forecast_dates['lag_6'] = 0
    forecast_dates['lag_7'] = 0
    forecast_dates['lag_8'] = 0
    forecast_dates['lag_9'] = 0
    forecast_dates['lag_10'] = 0
    forecast_dates['lag_11'] = 0
    forecast_dates['lag_12'] = 0
    forecast_dates['lag_13'] = 0
    forecast_dates['lag_14'] = 0

    model_price = joblib.load('ml/data_ml/model_price_2.pkl')
    model_units = joblib.load('ml/data_ml/model_cb-2.pkl')

    result = []
    for index, row in forecast_dates.iterrows():
        row['date'] = 1
        row_price = row[['st_id', 'pr_sku_id', 'date', 'pr_group_id',
                                    'pr_cat_id', 'pr_sales_type_id', 'pr_subcat_id',
                                    'pr_uom_id', 'st_city_id', 'st_division_id',
                                    'st_type_format_id', 'st_type_loc_id',
                                    'st_type_size_id', 'product_clasters',
                                    'price_clasters', 'holiday', 'dayofweek'

                                    ]]

        row['price'] = model_price.predict(row_price)

        try:
            rol7 = units.shift().rolling(7).mean()
            row['rol7'] = rol7.iloc[-1]
        except:
            pass

        try:
            rol14 = units.shift().rolling(14).mean()
            row['rol14'] = rol14.iloc[-1]
        except:
            row['rol14'] = 0

        try:
            row['pr_sales_min'] = units.shift().rolling(14).min()
            row['pr_sales_max'] = units.shift().rolling(14).max()
            row['pr_sales_median'] = units.shift().rolling(14).median()
            row['pr_sales_variance'] = units.shift().rolling(14).var()
        except:
            pass

        for lag in range(1, 15):
            try:
                row['lag_{}'.format(lag)] = units.iloc[-lag]
            except:
                continue

        row = row.fillna(0)

        row = row[['st_id', 'pr_sku_id', 'date', 'pr_sales_type_id', 'pr_group_id',
       'pr_cat_id', 'pr_subcat_id', 'pr_uom_id', 'st_city_id',
       'st_division_id', 'st_type_format_id', 'st_type_loc_id',
       'st_type_size_id', 'price', 'rol7', 'rol14', 'pr_sales_min',
       'pr_sales_max', 'pr_sales_median', 'pr_sales_variance', 'lag_1',
       'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7', 'lag_8', 'lag_9',
       'lag_10', 'lag_11', 'lag_12', 'lag_13', 'lag_14', 'dayofweek',
       'product_clasters', 'price_clasters', 'trend', 'trend_upper',
       'trend_lower', 'yhat', 'holiday']]

        row['pr_sales_max'] = 0
        row['pr_sales_min'] = 0
        row['pr_sales_median'] = 0
        row['pr_sales_variance'] = 0

        pred = model_units.predict(row)


        result.append(pred)


    forecast_dates = forecast_dates.fillna(0)
    forecast_dates['rol14'] = forecast_dates['rol14'].astype('float')
    forecast_dates['rol7'] = forecast_dates['rol7'].astype('float')
    forecast_dates['dayofweek'] = forecast_dates['dayofweek'].astype('int')
    forecast_dates['product_clasters'] = forecast_dates['product_clasters'].astype('int')
    forecast_dates['price_clasters'] = forecast_dates['price_clasters'].astype('int')

    return result