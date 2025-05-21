# pet-orch

## Описание

pet-orch — это шаблон проекта на FastAPI с интеграцией PostgreSQL, Redis, Prometheus, Grafana и Telegram-бота для получения метрик.

## Запуск проекта

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/FinnMem/pet-orch.git
   cd pet-orch
   ```

2. Создайте файл .env на основе .env.example и заполните необходимые переменные.

3. Запустите сервисы с помощью Docker Compose:

    ```bash
    docker compose up --build
    ```

4. Приложение будет доступно по адресу http://localhost:8000