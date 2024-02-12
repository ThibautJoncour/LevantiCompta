from project.wsgi import application

if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(["manage.py", "collectstatic", "--noinput"])
    execute_from_command_line(["manage.py", "migrate"])
    execute_from_command_line(["manage.py", "createsuperuser"])
    execute_from_command_line(["manage.py", "runserver"])
