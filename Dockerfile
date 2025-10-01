FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && grep -v "pywin32" requirements.txt > requirements_clean.txt \
    && pip install --prefer-binary -r requirements_clean.txt

# Copy source code (without .env, rely on docker-compose env_file)
COPY ./app ./app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


