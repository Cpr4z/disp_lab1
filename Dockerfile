# Используем официальный Python-образ
FROM python:3.10-slim

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код в контейнер
COPY . /app/

# Открываем порт для приложения
EXPOSE 8080

# Команда запуска
CMD ["sh", "-c", "python src/app/manage.py migrate && python src/app/manage.py collectstatic --noinput && python src/app/manage.py runserver 0.0.0.0:8080"]