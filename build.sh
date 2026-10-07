#!/bin/bash
# Build script for Vercel
set -e

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Make Migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."
mkdir -p staticfiles
python3 manage.py collectstatic --noinput --clear

echo "Seeding default users..."
python3 seed_default_users.py

echo "Done"
