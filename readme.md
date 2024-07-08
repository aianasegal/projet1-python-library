# Books Library Application

This project is a simple Books Library application built using Flask (Python) for the backend and HTML with Axios for the frontend.

## Overview

The Books Library application allows users to register, login, borrow books, and view both available and borrowed books. Admin users have additional privileges such as managing books and user roles.

## Accessing the Application

To access the Books Library application, follow these steps:

- Open a web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## User Operations

### Register

Use the `/register` endpoint to create a new user account.

### Login

Use the `/login` endpoint to authenticate and obtain an access token.

### View Books

Navigate to `/books` to view all available books.
- You can also borrow books using the provided form.

## Admin Operations

### Admin Dashboard

Access `/admin` (requires admin role) to perform administrative tasks such as CRUD operations on books and managing user roles.

## File Structure

- **`app.py`**: Flask application entry point.
- **`models.py`**: Defines SQLAlchemy models (`User` and `Book`).
- **`books.html`**: Frontend interface for the Books Library.
- **`login.html`**: Frontend interface for user login.

## Additional Notes

- Ensure all Flask extensions and required libraries (`Flask`, `SQLAlchemy`, etc.) are installed.
- Customize JWT secret key (`JWT_SECRET_KEY`) and database URI (`SQLALCHEMY_DATABASE_URI`) for production use.


