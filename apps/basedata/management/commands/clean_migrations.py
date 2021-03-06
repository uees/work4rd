import os
import shutil

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = '清除 migrations 数据'

    def handle(self, *args, **options):
        clean_migrations()
        self.stdout.write(self.style.SUCCESS('清除成功'))


def clean_migrations():
    for migrations_path in get_migrations_dirs():
        for item in os.listdir(migrations_path):
            if item != '__init__.py':
                item_path = os.path.join(migrations_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    shutil.rmtree(item_path)


def get_migrations_dirs():
    migrations_dirs = []
    apps_dir = os.path.join(settings.BASE_DIR, 'apps')
    for app_dir in os.listdir(apps_dir):
        app_path = os.path.join(apps_dir, app_dir)
        if os.path.isdir(app_path):
            app_migrations_path = os.path.join(app_path, 'migrations')
            if os.path.exists(app_migrations_path):
                migrations_dirs.append(app_migrations_path)
    return migrations_dirs
