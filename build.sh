#!/usr/bin/env bash
set -o errexit  # يوقف التنفيذ إذا في أي خطأ

echo "=== Starting Build Process ==="

# 1. تثبيت المكتبات
pip install -r requirements.txt

# 2. عمل الميغريشنز (بحذر)
echo "=== Checking for Migrations ==="
python manage.py makemigrations --check --dry-run

# 3. تطبيق الميغريشنز
echo "=== Running Migrations ==="
python manage.py migrate

# 4. جمع الملفات الثابتة
echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== Build Complete ==="