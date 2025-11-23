#!/usr/bin/env bash
set -o errexit

echo "=== Starting Build Process ==="
pip install -r requirements.txt

echo "=== Running Migrations ==="
python manage.py migrate

echo "=== Fixing Admin Permissions ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

# حاول تعديل user 'dalla'
try:
    user = User.objects.get(username='dalla')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print('✅ User dalla is now ADMIN!')
    print('🔑 Login with: username=dalla, your original password')
except Exception as e:
    print(f'⚠️  Could not find user dalla: {e}')
    # أنشئ admin جديد إذا 'dalla' ما موجود
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'Admin123456!')
        print('✅ New admin created!')
        print('🔑 Login with: username=admin, password=Admin123456!')
    else:
        print('ℹ️  Admin user already exists')
"

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== Build Complete ==="