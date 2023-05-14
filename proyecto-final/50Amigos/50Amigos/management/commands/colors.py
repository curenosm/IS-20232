from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Displays server\'s datetime'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        self.stdout.write('Available styles for stdout:')
        self.stdout.write(self.style.ERROR('ERROR'))
        self.stdout.write(self.style.NOTICE('NOTICE'))
        self.stdout.write(self.style.SUCCESS('SUCCESS'))
        self.stdout.write(self.style.WARNING('WARNING'))
        self.stdout.write(self.style.SQL_FIELD('SQL_FIELD'))
        self.stdout.write(self.style.SQL_COLTYPE('SQL_COLTYPE'))
        self.stdout.write(self.style.SQL_KEYWORD('SQL_KEYWORD'))
        self.stdout.write(self.style.SQL_TABLE('SQL_TABLE'))
        self.stdout.write(self.style.HTTP_INFO('HTTP_INFO'))
        self.stdout.write(self.style.HTTP_SUCCESS('HTTP_SUCCESS'))
        self.stdout.write(self.style.HTTP_NOT_MODIFIED('HTTP_NOT_MODIFIED'))
        self.stdout.write(self.style.HTTP_REDIRECT('HTTP_REDIRECT'))
        self.stdout.write(self.style.HTTP_NOT_FOUND('HTTP_NOT_FOUND'))
        self.stdout.write(self.style.HTTP_BAD_REQUEST('HTTP_BAD_REQUEST'))
        self.stdout.write(self.style.HTTP_SERVER_ERROR('SERVER_ERROR'))
        self.stdout.write(self.style.MIGRATE_HEADING('MIGRATE_HEADING'))
        self.stdout.write(self.style.MIGRATE_LABEL('MIGRATE_LABEL'))
        self.stdout.write('')

        self.stdout.write('Available colors for fg/bg:')
        self.stdout.write('black')
        self.stdout.write('red')
        self.stdout.write('green')
        self.stdout.write('yellow')
        self.stdout.write('blue')
        self.stdout.write('magenta')
        self.stdout.write('cyan')
        self.stdout.write('white')
        self.stdout.write('')

        self.stdout.write('Available options for roles:')
        self.stdout.write('bold')
        self.stdout.write('underscore')
        self.stdout.write('blink')
        self.stdout.write('reverse')
        self.stdout.write('conceal')
        self.stdout.write('')

        self.stdout.write('Example of establishment of roles:')
        self.stdout.write('export DJANGO_COLORS="role=fg/bg,option;role2=fg"')
        self.stdout.write(
            'export DJANGO_COLORS="error=yellow/blue,blink;notice=magenta"')
