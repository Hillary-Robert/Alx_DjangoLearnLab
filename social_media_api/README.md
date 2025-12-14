# Social Media API (Django + DRF) — Project Setup & Authentication

## Repo
- GitHub: Alx_DjangoLearnLab
- Directory: social_media_api

## Features (Stage 0)
- Django project + accounts app
- Custom User model (extends AbstractUser)
  - bio (TextField)
  - profile_picture (ImageField)
  - followers (ManyToMany to self, symmetrical=False)
- Token Authentication (DRF authtoken)
- Endpoints:
  - POST /api/accounts/register/  -> returns token
  - POST /api/accounts/login/     -> returns token
  - GET  /api/accounts/profile/   -> authenticated user profile
  - PUT  /api/accounts/profile/   -> update profile

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install django djangorestframework djangorestframework-authtoken pillow
django-admin startproject social_media_api
cd social_media_api
python manage.py startapp accounts
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
