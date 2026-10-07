#!/bin/bash
# Build script for Vercel
set -ex

echo "Starting build process..."

echo "Checking Python and Pip versions..."
python3 --version || python --version
python3 -m pip --version || pip --version

echo "Installing requirements..."
python3 -m pip install -r requirements.txt --break-system-packages || python3 -m pip install -r requirements.txt

echo "Make Migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."
mkdir -p staticfiles
python3 manage.py collectstatic --noinput --clear

echo "Seeding default users..."
python3 seed_default_users.py

echo "Build process completed successfully!"
