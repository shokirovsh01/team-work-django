from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создаёт группы Patient, Doctor, Admin'

    def handle(self, *args, **options):
        for name in ['Patient', 'Doctor', 'Admin']:
            group, created = Group.objects.get_or_create(name=name)
            status = 'создана' if created else 'уже была'
            self.stdout.write(f'{name}: {status}')