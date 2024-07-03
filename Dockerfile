# Pull official base image
FROM python:3.12-slim-bullseye

# update kernal & install libraries
RUN apt-get update && apt-get -y install gcc libqp-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]