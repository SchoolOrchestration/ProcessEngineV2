'''
# run every 60 seconds:
Usage: python manage.py run_tasks --interval 60
'''
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from api.models import Task

from datetime import datetime
import time


class Command(BaseCommand):
    help = 'Safely run tasks forever'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=300,
            help='Interval between runs in seconds.'
        )


    def handle(self, *args, **options):
        wait_time = options.get('interval', 300)
        run_statuses = ['N', 'F']

        print("Running tasks every {} seconds".format(wait_time))

        while True:
            tasks_to_run = Task.objects.filter(
                status__in = run_statuses,
            )
            print("Running tasks.")
            for task in tasks_to_run:
                if task.should_run():
                    task = task.run()
                    print("Ran: {} at {}".format(
                        task.id,
                        datetime.now().isoformat()
                    ))
                else:
                    print('Skipping {}'.format(task.id))
            time.sleep(wait_time)