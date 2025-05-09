# Arktech Blog - Deployment Guide

This README provides all the steps and configurations needed to deploy the Blog to production.

---

## Requirements

* Python 3.12
* PostgreSQL database (configured via `.env`)
* Gunicorn (installed via Poetry)
* Docker (this project is fully Docker-ready and intended for containerized deployment)
* Hostinger server

---

## Environment Configuration

Prepare a `.env` file in the project root with the following keys:

```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your_db_host
DATABASE_PORT=5432

MEDIA_ROOT=/home/hostinger_user/public_html/media
STATIC_ROOT=/app/staticfiles

CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourfrontend.com,https://www.yourfrontend.com
```

Important:

* For early testing, you can temporarily set `CORS_ALLOW_ALL_ORIGINS=True`.
* In production, switch it to `False` and define exact frontend domains.

---

## Setup Commands

### Build and run with Docker

```
docker compose up --build
```

### Run migrations inside the container

```
docker compose exec web python manage.py migrate
```

### Collect static files inside the container

```
docker compose exec web python manage.py collectstatic
```

The `Dockerfile` is configured to run Gunicorn in production.

---

## Static and Media Files

* Static files: Served from `STATIC_ROOT` (after running `collectstatic`)
* Media files: Stored in `MEDIA_ROOT`, must be served directly by the web server (Apache or Nginx)

Note: Django does NOT serve static or media files in production.

---

## CORS Setup

* Allow cross-origin requests only from trusted frontend domains.
* Update `CORS_ALLOWED_ORIGINS` in `.env` accordingly.

---

## Final Checks

* `DEBUG=False` in production
* `ALLOWED_HOSTS` set correctly
* Database credentials are secure
* Gunicorn runs inside Docker
* Static and media files are correctly configured on the server
* CORS only allows trusted origins

# API Documentation

This section provides a clear overview of the available API endpoints for the frontend to integrate with.

---

## Base URL

**Production backend:**
[https://arktech-backend.onrender.com](https://arktech-backend.onrender.com)

---

## Authentication

### Obtain JWT Token

**POST** `/api/auth/token/`

**Body (JSON):**

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### Refresh JWT Token

**POST** `/api/auth/token/refresh/`

**Body (JSON):**

```json
{
  "refresh": "<refresh_token>"
}
```

**Response:**

```json
{
  "access": "<new_access_token>"
}
```

---

## Posts

### List All Posts (Public)

**GET** `/api/posts/`

**Query Parameters (optional):**

* `tag`: Filter by tag (e.g., `?tag=Cybersecurity`)

### Retrieve Single Post (Public)

**GET** `/api/posts/{id}/`

### Create Post (Staff Only)

**POST** `/api/posts/`

**Headers:**

* `Authorization: Bearer <access_token>`

**Body (multipart/form-data):**

* `title`: string
* `subtitle`: string
* `tags`: JSON array (e.g., `["Software Development", "Cybersecurity"]`)
* `paragraphs`: JSON array (e.g., `[{"title": "Intro", "content": "Text"}, {"content": "More text"}]`)
* `cta`: string (Markdown supported)
* `image`: file upload (JPEG or PNG)

### Update Post (Staff Only)

**PATCH** `/api/posts/{id}/`

**Headers:**

* `Authorization: Bearer <access_token>`

**Body (JSON):**

```json
{
  "title": "Updated Title"
}
```

### Delete Post (Staff Only)

**DELETE** `/api/posts/{id}/`

**Headers:**

* `Authorization: Bearer <access_token>`

---

## Users (Admin/Superuser Only)

The users API is protected by the `IsSuperUserOrReadOnly` permission, meaning only superusers can perform modifications.

### List All Users

**GET** `/api/users/`

**Headers:**

* `Authorization: Bearer <access_token>`

### Retrieve Single User

**GET** `/api/users/{id}/`

**Headers:**

* `Authorization: Bearer <access_token>`

### Create User (Sets is\_staff = true by default)

**POST** `/api/users/`

**Headers:**

* `Authorization: Bearer <access_token>`

**Body (JSON):**

```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "securepassword"
}
```

### Update User

**PATCH** `/api/users/{id}/`

**Headers:**

* `Authorization: Bearer <access_token>`

**Body (JSON):**

```json
{
  "email": "updated@example.com",
  "username": "updatedusername"
}
```

### Delete User

**DELETE** `/api/users/{id}/`

**Headers:**

* `Authorization: Bearer <access_token>`

---

## Notes for Frontend

* When the access token expires, use the refresh token endpoint to get a new one.
* Always send `tags` and `paragraphs` as JSON strings in multipart requests.
* Public endpoints (list and retrieve posts) do not require authentication.
