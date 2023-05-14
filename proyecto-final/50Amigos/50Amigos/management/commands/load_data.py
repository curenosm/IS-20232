from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Loads fixtures found on the default folder'

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

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED('Fixtures are being loaded...')
        )
        for element in settings.FIXTURE_MODELS:
            try:
                call_command(
                    'loaddata',
                    f'fixtures/{element}.json',
                    verbosity=0)
                self.stdout.write(self.style.SUCCESS(element))
            except Exception:
                self.stdout.write(self.style.ERROR(f'!!! {element}'))
        pass
