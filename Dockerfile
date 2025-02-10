FROM python:3.10

# Создаем пользователя без прав root
RUN useradd -m appuser
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Создаем виртуальное окружение
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Устанавливаем зависимости в виртуальное окружение
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY recipes_project/ /app/

# Переключаемся на пользователя appuser
USER appuser

# Команда для запуска приложения
CMD ["gunicorn", "recipes_project.wsgi:application", "--bind", "0.0.0.0:8000"]