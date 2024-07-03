# MyProject

## Introduction

MyProject is a Django-based API project with JWT authentication, email login with OTP, media file handling, and CRUD operations. The project uses PostgreSQL as the database and follows the MVC pattern.

## Features

- JWT Authentication
- Email Login with OTP
- Media File Handling
- CRUD Operations

## Requirements

- Python 3.x
- Docker
- Docker Compose

## Setup

### Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/myproject.git
   cd myproject
   ```

2. Install dependencies:
    ```
   pip install -r requirements.txt
   ```

3. Configure the database in project/settings.py.

4. Run migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```
    python manage.py createsuperuser
    ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## Docker Setup

1. Build and run the Docker containers:
    ```
    docker-compose up --build
    ```
2. The application will be accessible at http://localhost:8000.


## API Endpoints

Register: POST /api/register/
OTP Login Request: POST /api/otp-login/
OTP Login Verify: PUT /api/otp-login/
Upload Media: POST /api/media/
List Media: GET /api/media/
Media Detail: GET, PUT, DELETE /api/media/<id>/