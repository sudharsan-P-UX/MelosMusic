#!/bin/bash
# Build script for Vercel

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Make Migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

echo "Seeding default users..."
python seed_default_users.py

echo "Done"
