# API

## Introduction

API is a robust Django-based RESTful API designed to facilitate a modern reporting system. It integrates essential features including secure JWT authentication, OTP-based email login for heightened security, advanced media file management capabilities, and efficient CRUD operations across various data entities. Developed with PostgreSQL as the database backend, the project follows the Model-View-Controller (MVC) architectural pattern, ensuring scalability, maintainability, and optimal performance.


## Features

- 🔒 **JWT Authentication**: Securely authenticate users and authorize access.
- 📧 **Email Login with OTP**: Authenticate users via email using OTP for added security.
- 🖼️ **Media File Handling**: Upload, retrieve, update, and delete media files (photos, videos, PDFs).
- 🔄 **CRUD Operations**: Perform CRUD (Create, Read, Update, Delete) operations for users, reports, and media files.

## Functionality

### User Management

- **Register**: Allows users to create a new account using username, email, and password.
- **OTP Login**: Authenticate users via email OTP for login.
- **Profile Management**: Update user profile information including full name, date of birth, gender, address, and national ID.

### Media Management

- **Upload Media**: Upload various types of media files (photos, videos, PDFs) to the system.
- **List Media**: Retrieve a list of all media files uploaded by the authenticated user.
- **Media Detail**: View details of a specific media file, update its contents, or delete it.

### Reporting

- **Create Report**: Generate reports detailing incidents, including textual description and associated media files.
- **List Reports**: Retrieve a list of reports submitted by the authenticated user.
- **Report Detail**: View, update, or delete a specific report including its description and associated media files.


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


# API Documentation

### Swagger UI

API documentation is available using Swagger UI. After starting the development server or Docker containers, navigate to http://localhost:8000/swagger/ to interactively explore and test the API endpoints.

## API Endpoints

### Register
- **Method**: POST
- **Endpoint**: `/api/register/`
- **Description**: Register a new user.

### OTP Login Request
- **Method**: POST
- **Endpoint**: `/api/otp-login/`
- **Description**: Request an OTP for login.

### OTP Login Verify
- **Method**: PUT
- **Endpoint**: `/api/otp-login/`
- **Description**: Verify OTP and login.

### Upload Media
- **Method**: POST
- **Endpoint**: `/api/media/`
- **Description**: Upload a new media file.

### List Media
- **Method**: GET
- **Endpoint**: `/api/media/`
- **Description**: List all media files of the logged-in user.

### Media Detail
- **Method**: GET, PUT, DELETE
- **Endpoint**: `/api/media/<id>/`
- **Description**: Retrieve, update, or delete a media file by ID.

### Create Report
- **Method**: POST
- **Endpoint**: `/api/reports/`
- **Description**: Create a new report with multiple media files.

### List Reports
- **Method**: GET
- **Endpoint**: `/api/reports/`
- **Description**: List all reports of the logged-in user.

### Report Detail
- **Method**: GET, PUT, DELETE
- **Endpoint**: `/api/reports/<id>/`
- **Description**: Retrieve, update, or delete a report by ID.

