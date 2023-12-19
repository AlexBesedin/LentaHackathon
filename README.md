# Хакатон Лента

Задача: создание предсказательной модели и его интерфейса по прогнозированию спроса на товары заказчика собственного производства ООО “Лента”.

## Бэкенд-разработчики:
- [Беседин Алексей](https://github.com/AlexBesedin)
- [Карина Виктория](https://github.com/vic-k-777)

## Data Science:
- [Daria Kashina](https://github.com/daria-kashina)
- [Pavel Fetisov](https://github.com/tupperq)

## Архитектура бэкенд системы

- Django приложение: основной компонент системы, который обрабатывает входящие HTTP-запросы и взаимодействует с другими компонентами системы
- БД, отвечает за хранение исторических и прогнозируемых данных
- ML выполняет прогнозирование продаж.
- Redis, используется как брокер сообщений для Celery, чтобы организовать очередь задач, которые будут обрабатываться в фоновом режиме.
- Celery, система для асинхронной обработки задач в фоновом режиме.
- Flower, веб-интерфейс для мониторинга и управления задачами Celery.

## Cтэк технологий

- Python 3.11
- Django 4.2.5
- Django REST Framework 3.14
- PostgreSQL
- Redis 
- Celery
- Celery Flower
- Celery Beat
- Docker
- Nginx

## Подготовка и запуск проекта

### Склонируйте репозиторий:
```sh
git clone git@github.com:AlexBesedin/LentaHackathon.git
```

### Создайте файл содержащий переменные виртуального окружения (.env)
```sh
cd LentaHackathon/infra
touch .env
```

```sh
SECRET_KEY = <Секретный ключ>
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
### Разверните контейнеры и выполните миграции:
```sh
cd LentaHackathon/infra/
sudo docker-compose up -d --build
sudo docker-compose exec backend python manage.py migrate
```
Создайте суперюзера и соберите статику::
```sh
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
### Загрузите магазины, категории и продажи в базу данных:
```sh
sudo docker-compose exec backend python manage.py import_stores
sudo docker-compose exec backend python manage.py import_categories
sudo docker-compose exec backend python manage.py import_sales
```
### Запуск Задачи Celery Вручную
#### *Примечание: Данная команда запустит инференс прогноза, который сделает запросы в базу данных, после передаст данные в DS модель, и полученный прогноз от DS модели запишет в базу данных в модель Forecast.

```sh
sudo docker-compose exec backend celery -A lenta_main call lenta_main.tasks.main
```
#### * На продакшене, необходимо выставить время, когда будет выполняться асинхронная задача прогноза. Выполнение задачи будет происходит в фоновом режиме.

```sh
CELERY_BEAT_SCHEDULE = {
    'run_main_every_10_min': {
        'task': 'lenta_main.tasks.main',
        'schedule': timedelta(minutes=10),
    },
}
```
#### Celery Flower позволяет отслеживать состояние и прогресс выполнения задач, а также управлять задачами и рабочими процессами в вашем Celery-кластере через веб-интерфейс. 

```sh
http://localhost:5555/
```

### Документация
API документация будет доступна по адресу:

```sh
 http://ваш_ip_адрес/api/docs/
```

#### UPDATE: Необходимо [скачать](https://disk.yandex.ru/d/Yfh_yjdajSSc4A) обученную ML модель, и поместить её в папку backend/ml/data_ml .
