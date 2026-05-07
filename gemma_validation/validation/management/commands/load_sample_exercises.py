"""
Management command to load sample data
"""
from django.core.management.base import BaseCommand
from validation.sample_data import load_sample_exercises


class Command(BaseCommand):
    help = 'Load sample Japanese N3 exercises'

    def handle(self, *args, **options):
        created = load_sample_exercises()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {created} sample exercises')
        )
