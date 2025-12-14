import time
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        max_retries = 30
        retries = 0
        
        while not db_up and retries < max_retries:
            try:
                self.check(databases=['default'])
                db_up = True
                self.stdout.write(self.style.SUCCESS('✅ Database available!'))
            except (Psycopg2OpError, OperationalError) as e:
                retries += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'❌ Database unavailable, waiting 1 second... (Attempt {retries}/{max_retries})'
                    )
                )
                time.sleep(1)
        
        if not db_up:
            self.stdout.write(
                self.style.ERROR('💥 Could not connect to database after maximum retries!')
            )
            raise OperationalError("Database connection failed")