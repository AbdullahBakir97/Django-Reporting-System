# API

## Introduction

API is a Django-based API project with JWT authentication, email login with OTP, media file handling, and CRUD operations. The project uses PostgreSQL as the database and follows the MVC pattern.

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

### User Registration

- **Register a New User**
  - **Method & Endpoint**: `POST /api/register/`
  - **Description**: Registers a new user with the provided credentials.

### OTP-Based Authentication

- **Request OTP for Login**
  - **Method & Endpoint**: `POST /api/otp-login/`
  - **Description**: Requests an OTP for user login.

- **Verify OTP for Login**
  - **Method & Endpoint**: `PUT /api/otp-login/`
  - **Description**: Verifies the OTP and logs in the user.

### Media Management

- **Upload Media**
  - **Method & Endpoint**: `POST /api/media/`
  - **Description**: Uploads a new media file.

- **List All Media**
  - **Method & Endpoint**: `GET /api/media/`
  - **Description**: Retrieves a list of all media files.

- **Media Detail**
  - **Method & Endpoint**: `GET, PUT, DELETE /api/media/<id>/`
  - **Description**: Retrieves, updates, or deletes a specific media file by its ID.
