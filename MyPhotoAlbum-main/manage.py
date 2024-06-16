import os
import sys
from django.core.management import execute_from_command_line

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photoshare.settings')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
# sudo nohup python3 manage.py runserver 0.0.0.0:80 &