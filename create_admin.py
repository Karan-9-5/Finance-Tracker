import os
import django
from django.contrib.auth import get_user_model

def create_admin():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword' # You can change this
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == "__main__":
    create_admin()
