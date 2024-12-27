FROM python:latest

WORKDIR /app

# Копируем файлы в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


COPY config.toml /app/config.toml

# Указываем команду запуска по умолчанию
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

