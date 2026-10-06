import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ftsapp.settings')
django.setup()

from django.contrib.auth.models import User
from mainapp.models import LoginInfo
from adminapp.models import Department

def init_database():
    print("Running initial database setup...")

    # 1. Ensure Django Superuser exists (for /softproadmin/)
    admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@gmail.com')
    admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345')

    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        print(f"Created Django superuser: {admin_username}")
    else:
        print(f"Django superuser '{admin_username}' already exists.")

    # 2. Ensure LoginInfo admin exists (for /adminlogin/)
    if not LoginInfo.objects.filter(email=admin_email, usertype='admin').exists():
        LoginInfo.objects.create(
            usertype='admin',
            email=admin_email,
            password=admin_password
        )
        print(f"Created LoginInfo admin: {admin_email} (password: {admin_password})")
    else:
        print(f"LoginInfo admin '{admin_email}' already exists.")

    # 3. Ensure standard initial departments exist
    default_departments = ['Human Resources', 'Development', 'Accounts & Finance', 'Operations']
    for dept_name in default_departments:
        dept, created = Department.objects.get_or_create(deptname=dept_name)
        if created:
            print(f"Created department: {dept_name}")

    print("Initial database setup completed successfully.")

if __name__ == '__main__':
    init_database()
