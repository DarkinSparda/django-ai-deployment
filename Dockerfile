# STEP 1: Choose the base image
# We're using Python 3.12 on a lightweight Linux system (Alpine)
# Alpine is small and fast, perfect for production
FROM python:3.12-slim

# STEP 2: Set environment variables
# Prevents Python from writing .pyc files (compiled bytecode)
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to terminal (useful for logs)
ENV PYTHONUNBUFFERED=1

# STEP 3: Set the working directory inside the container
# All commands will run from this directory
WORKDIR /app

# STEP 4: Install system dependencies
# Update package list and install PostgreSQL client library
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# STEP 5: Copy requirements first (for Docker layer caching)
# This means if requirements don't change, Docker won't reinstall them
COPY backend/ai_blog_app/requirements.txt /app/

# STEP 6: Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# STEP 7: Copy the entire Django project
COPY backend/ai_blog_app/ /app/

# STEP 8: Copy frontend templates into the container
COPY frontend /frontend

# STEP 9: Create media directory for user uploads
RUN mkdir -p /app/media

# STEP 10: Expose the port Django will run on
EXPOSE 8000

# STEP 11: Run database migrations and start the server
# We use gunicorn (production WSGI server) instead of Django's dev server
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn ai_blog_app.wsgi:application --bind 0.0.0.0:8000 --workers 3
