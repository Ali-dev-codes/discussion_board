#!/usr/bin/env bash
set -o errexit

echo "=== Starting Build Process ==="

# تثبيت المكتبات
pip install -r requirements.txt

echo "=== Running Migrations ==="
python manage.py migrate

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== Build Complete Successfully ==="
