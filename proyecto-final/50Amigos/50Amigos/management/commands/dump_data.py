import os
import time

from io import StringIO

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Dumps data for models indicated in settings.FIXTURE_LIST'

    def add_arguments(self, parser):
        # Positional argument
        # parser.add_argument(
        #       'name',
        #       type=int,
        #       help='Msg'
        # )

        # Optional argument
        # parser.add_argument(
        #       '-p', '--prefix',
        #       type=str,
        #       help='Define a username prefix'
        # )

        # Flag
        # parser.add_argument(
        #       '-a', '--admin',
        #       action='store_true',
        #       help='Create an admin account'
        # )
        pass

    def handle(self, *args, **kwargs):
        # name = kwargs.get('name', '123')
        output_dir = os.path.join(settings.BASE_DIR, 'fixtures')
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED('Fixtures are being generated...')
        )
        if os.path.exists(output_dir):
            for element in settings.FIXTURE_MODELS:
                app_name, model_name = element.split('.')
                try:
                    buf = StringIO()
                    call_command('dumpdata', element, stdout=buf)
                    buf.seek(0)
                    with open(f'{output_dir}/{element}.json', 'w') as f:
                        f.write(buf.read())
                    self.stdout.write(self.style.SUCCESS(element))
                except Exception:
                    self.stdout.write(self.style.ERROR(f'!!! {element}'))
        else:
            self.stdout.write(self.style.ERROR(output_dir + 'Does not exists'))
            os.makedirs(output_dir)


            # time.sleep(0.5)
            # if not counter%2:
            #     # call_command('dumpdata', element, verbosity=0)
            #     self.stdout.write(self.style.SUCCESS(element))
            # else:
            #     self.stdout.write(self.style.ERROR(element))
            # counter += 1
