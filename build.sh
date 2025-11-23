#!/usr/bin/env bash
set -o errexit

echo "=== Starting Build Process ==="
pip install -r requirements.txt

echo "=== Running Migrations ==="
python manage.py migrate

echo "=== CREATING NEW ADMIN ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

# أنشئ admin جديد
User.objects.create_superuser(
    username='superadmin',  # اسم جديد
    email='superadmin@example.com',
    password='Super123!'    # كلمة سر قوية
)
print('✅ NEW ADMIN CREATED!')
print('👤 Username: superadmin')
print('🔑 Password: Super123!')
print('📧 Email: superadmin@example.com')
"

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== Build Complete ==="