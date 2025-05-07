# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.2

# Set work directory
WORKDIR /opt/pysetup

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy project files
COPY pyproject.toml poetry.lock* /opt/pysetup/

# Install without virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-root \
    && poetry run pip install --upgrade pip

# Copy full project
COPY . /opt/pysetup/

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
