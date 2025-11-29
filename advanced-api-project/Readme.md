# Advanced API Project (Django REST Framework)

## Project Overview

This project implements a structured and extensible RESTful API using Django and Django REST Framework (DRF). The API provides endpoints for managing authors and books, supports nested serialization, includes custom validation, and implements filtering, searching, and ordering.

---

## Technologies Used

* Python
* Django
* Django REST Framework
* django-filter
* SQLite (development database)

---

## Installation

### 1. Create project folder

```bash
mkdir advanced-api-project
cd advanced-api-project
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# or
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install django djangorestframework django-filter
```

### 4. Start Django project

```bash
django-admin startproject advanced_api_project .
```

### 5. Create API app

```bash
python manage.py startapp api
```

---

## Project Structure

```
advanced-api-project/
│
├── advanced_api_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── test_views.py
│   └── admin.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## Models

Models are located in **api/models.py**.

### Author

* name

### Book

* title
* publication_year
* author (ForeignKey to Author)

Relationship: One Author → Many Books

### Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Serializers

Serializers are located in **api/serializers.py**.

### BookSerializer

* Serializes all book fields
* Validates that `publication_year` is not in the future

### AuthorSerializer

* Serializes author name
* Includes related books using `BookSerializer(many=True)`

---

## API Views

Views are located in **api/views.py**.

### BookListView

Handles:

* `GET /api/books/`
* `POST /api/books/`

Supports:

* Filtering
* Searching
* Ordering

### BookDetailView

Handles:

* `GET /api/books/<id>/`
* `PUT /api/books/<id>/`
* `PATCH /api/books/<id>/`
* `DELETE /api/books/<id>/`

---

## URL Configuration

### api/urls.py

```python
path("books/", BookListView.as_view(), name="book-list")
path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail")
```

### advanced_api_project/urls.py

```python
path("api/", include("api.urls"))
```

---

## Filtering, Searching, and Ordering

### Filtering

```
/api/books/?title=Things
/api/books/?publication_year=2000
/api/books/?author__name=John
```

### Searching

```
/api/books/?search=stories
/api/books/?search=author
```

### Ordering

```
/api/books/?ordering=title
/api/books/?ordering=-publication_year
```

---

## Running the Server

```bash
python manage.py runserver
```

API base endpoint:

```
http://127.0.0.1:8000/api/books/
```

---

## Running Unit Tests

Tests are located in **api/test_views.py**.

Run tests:

```bash
python manage.py test api
```

A separate test database is created automatically for testing.

---

## Example API Requests

### Create a Book

```http
POST /api/books/
{
  "title": "Things Fall Apart",
  "publication_year": 1958,
  "author": 1
}
```

### Filter by Year

```
GET /api/books/?publication_year=1958
```

### Search

```
GET /api/books/?search=fall
```

### Order

```
GET /api/books/?ordering=-publication_year
```

---

## Completed Features

* Django project setup
* Author and Book models
* Custom and nested serializers
* Field validation
* Filtering (django-filter)
* Searching (DRF SearchFilter)
* Ordering (DRF OrderingFilter)
* CRUD API endpoints
* Unit tests for all main functionalities
* Project documentation
