# django-upscale-and-interpolate-video

Проект **django-upscale-and-interpolate-video** представляет собой веб-приложение для повышения разрешения и интерполяции видео с использованием моделей машинного обучения. Приложение разработано на Django и упаковано с помощью Docker для упрощённого развёртывания и масштабирования.

## Содержание

- [Требования](#требования)
- [Начало работы](#начало-работы)
  - [1. Проверьте установку Docker](#1-проверьте-установку-docker)
  - [2. Склонируйте репозиторий](#2-склонируйте-репозиторий)
  - [3. Загрузите веса моделей](#3-загрузите-веса-моделей)
  - [4. Запустите Docker Compose](#4-запустите-docker-compose)

## Требования

Перед началом работы убедитесь, что на вашем компьютере установлены следующие инструменты:

- [Docker](https://www.docker.com/get-started) (версия 20.10 или выше)
- [Docker Compose](https://docs.docker.com/compose/install/) (версия 1.29 или выше)
- [Git](https://git-scm.com/downloads)
- Python >= 3.8

## Начало работы

Следуйте этим инструкциям, чтобы получить копию проекта и запустить его на своей локальной машине для разработки и тестирования.

### 1. Проверьте установку Docker

Убедитесь, что Docker установлен и работает корректно. Для этого выполните следующую команду в терминале:

```bash
docker --version
```

Вы должны увидеть информацию о версии Docker, например:

```
Docker version 20.10.7, build f0df350
```

Также проверьте, что Docker Compose установлен:

```bash
docker compose version
```

Пример вывода:

```
Docker Compose version v2.1.1
```

Если Docker или Docker Compose не установлены, следуйте официальным [инструкциям по установке Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

### 2. Склонируйте репозиторий

Скопируйте репозиторий на свой локальный компьютер с помощью Git:

```bash
git clone https://github.com/msrbl/django-upscale-and-interpolate-video.git
cd django-upscale-and-interpolate-video
```

### 3. Загрузите веса моделей

Скачайте веса моделей по следующей ссылке:

[Скачать веса](https://drive.google.com/file/d/1gViYvvQrtETBgU1w8axZSsr7YUuw31uy/view)

После загрузки распакуйте архив и переместите папку `train_log` в директорию `./builds/rife` внутри проекта:

```bash
mv path_to_downloaded_train_log ./builds/rife/
```

Убедитесь, что структура папок соответствует требованиям проекта.

### 4. Запустите Docker Compose

Запустите все сервисы проекта с помощью Docker Compose:

```bash
docker compose up
```

Эта команда создаст и запустит необходимые контейнеры, установит зависимости и запустит веб-приложение. После успешного запуска API документацию можете посмотреть по адресу `http://localhost:8000/swagger`.