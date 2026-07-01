# FastAPI CRUD

A small FastAPI app for managing contacts, with session-based user registration/login in front of it.

## Features

- Register / login / logout with bcrypt-hashed passwords and cookie sessions
- Contact list with add, edit, and delete
- Header (username + logout) and footer (copyright), toggleable per page via `show_header` / `show_footer` query params

## Requirements

- Python 3.10+
- MySQL server reachable at `localhost:3307` (see `database.py`)

## Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Create the database and tables:

   ```sql
   CREATE DATABASE fastapi_db;

   USE fastapi_db;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL
   );

   CREATE TABLE contacts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL
   );
   ```

3. Update `database.py` if your MySQL host, port, user, or password differ from the defaults.

4. Run the app:

   ```
   uvicorn main:app --reload
   ```

5. Open `http://127.0.0.1:8000/register` to create an account, then log in.

## Routes

| Method | Path            | Description                  |
|--------|-----------------|------------------------------|
| GET    | /register       | Registration form            |
| POST   | /register       | Create account                |
| GET    | /login          | Login form                   |
| POST   | /login          | Authenticate, start session   |
| GET    | /logout         | Clear session                |
| GET    | /               | Contact list (auth required) |
| GET    | /add            | Add-contact form              |
| POST   | /add            | Create contact                |
| GET    | /edit/{id}      | Edit-contact form             |
| POST   | /edit/{id}      | Update contact                |
| GET    | /delete/{id}    | Delete contact                |
