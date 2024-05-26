# Library Management System

This project is a Library Management System built with Django and Django REST framework. It provides functionalities for users to view, search, and filter a list of books and reserve books. Additionally, it includes a management command to automatically remove expired book reservations.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Management Commands](#management-commands)
- [License](#license)

## Features

- User registration and authentication
- View, search, and filter books
- Book reservation for 1 day
- Automatic removal of expired reservations
- Pagination for book lists

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST framework
- Django Filter
- SimpleJWT

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/library-management-system.git
    cd library-management-system
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Usage

1. **Register and Login:**

    Use the `/api/register/` endpoint to create a new user and the `/api/token/` endpoint to obtain a JWT token.

2. **Access Book List and Details:**

    Use the `/api/books/` endpoint to view the list of books. You can filter, search, and paginate the list.

3. **Reserve a Book:**

    Use the `/api/reservations/` endpoint to reserve a book. Ensure you include the JWT token in the Authorization header.

4. **Mark a Book as Returned:**

    Use the `/api/borrowing/<id>/return/` endpoint to mark a book as returned.

## API Endpoints

### User Registration and Authentication

- **Register**: `POST /api/register/`
  - Body: `{ "username": "user", "password": "pass", "email": "email@example.com", ... }`
- **Login**: `POST /api/token/`
  - Body: `{ "username": "user", "password": "pass" }`

### Books

- **List Books**: `GET /api/books/`
  - Query Parameters: `search`, `filter`, `page`
- **Book Details**: `GET /api/books/<id>/`

### Reservations

- **Create Reservation**: `POST /api/reservations/`
  - Body: `{ "book": <book_id> }`
  - Headers: `Authorization: Bearer <token>`
- **Cancel Reservation**: `DELETE /api/reservations/<id>/`
  - Headers: `Authorization: Bearer <token>`

### Borrowing

- **Mark as Returned**: `POST /api/borrowing/<id>/return/`
  - Headers: `Authorization: Bearer <token>`

## Management Commands

- **Remove Expired Reservations**: `python manage.py remove_expired_reservations`

## Detailed API Usage

### User Registration and Login

#### Register a New User:

- **Endpoint:** `POST /api/register/`
- **Body:**
    ```json
    {
        "username": "john_doe",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "personal_number": "1234567890",
        "birth_date": "1990-01-01"
    }
    ```

#### Login:

- **Endpoint:** `POST /api/token/`
- **Body:**
    ```json
    {
        "username": "john_doe",
        "password": "securepassword"
    }
    ```
- **Response:**
    ```json
    {
        "access": "your_access_token",
        "refresh": "your_refresh_token"
    }
    ```

### Accessing Book List and Details

#### List Books:

- **Endpoint:** `GET /api/books/`
- **Query Parameters:** `search`, `filter`, `page`
- **Example Request:** `GET /api/books/?search=Harry&page=2`
- **Response:**
    ```json
    [
        {
            "id": 1,
            "title": "Harry Potter and the Sorcerer's Stone",
            "author": "J.K. Rowling",
            "quantity": 3,
            
        }
        
    ]
    ```

#### Book Details:

- **Endpoint:** `GET /api/books/<id>/`
- **Example Request:** `GET /api/books/1/`
- **Response:**
    ```json
    {
        "id": 1,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "quantity": 3
    }
    ```

### Reserving a Book

#### Create Reservation:

- **Endpoint:** `POST /api/reservations/`
- **Headers:** `Authorization: Bearer <your_access_token>`
- **Body:**
    ```json
    {
        "book": 1
    }
    ```

#### Cancel Reservation:

- **Endpoint:** `DELETE /api/reservations/<id>/`
- **Headers:** `Authorization: Bearer <your_access_token>`

