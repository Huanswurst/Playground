@echo off
start "npm dev" npm run dev
cd backend
start "django server" python manage.py runserver