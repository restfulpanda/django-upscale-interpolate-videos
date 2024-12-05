# django-upscale-and-interpolate-video

### Get started

1. Скачайте проект:
    ```bash
    git clone https://github.com/msrbl/django-upscale-and-interpolate-video
    cd django-upscale-and-interpolate-video
2. Установите зависимости:
    ```bash
    python -m venv UIdjango
    ./UIdjango/Scripts/activate
    pip install -r requirements.txt
3. Запустите контейнер Docker с redis
4. В файле /config/settings.py измените порт подключения к редис в переменных окружения:
```
CELERY_BROKER_URL = 'redis://user:pass@127.0.0.1:port/0'
CELERY_RESULT_BACKEND = 'redis://user:pass@127.0.0.1:port/1'
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:port",
    }
}
```
5. Запустите сервер celery:
    ```bash
    celery -A logic worker
6. Запустите сервер Django:
    ```bash
    python manage.py runserver
7. Пользуйтесь!
