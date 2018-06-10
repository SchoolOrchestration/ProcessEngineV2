from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from api.api import get_tasks_by_module_string

class Command(BaseCommand):
    help = 'register tasks'

    def handle(self, *args, **options):
        """
        Command that registers local tasks with the process engine
        """
        pass