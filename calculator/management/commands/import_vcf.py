from django.core.management.base import BaseCommand
from django.db import connection
from calculator.models import VCFTable
import os
import re

class Command(BaseCommand):
    help = 'Import VCF data from a SQL file'

    def add_arguments(self, parser):
        parser.add_argument(
            'sql_file',
            type=str,
            help='Path to the SQL file containing VCF data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing VCF data before importing'
        )

    def handle(self, *args, **options):
        sql_file = options['sql_file']
        clear_existing = options['clear']

        if not os.path.exists(sql_file):
            self.stdout.write(
                self.style.ERROR(f'SQL file not found: {sql_file}')
            )
            return

        if clear_existing:
            self.stdout.write('Clearing existing VCF data...')
            VCFTable.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Existing VCF data cleared.')
            )

        self.stdout.write(f'Importing VCF data from {sql_file}...')

        try:
            with open(sql_file, 'r') as file:
                content = file.read()
            
            self.stdout.write(f'File size: {len(content)} characters')

            # Parse SQL content and extract VCF data
            # Handle the format: INSERT INTO table60b (...) VALUES (...), (...), (...)
            insert_pattern = r'INSERT\s+INTO\s+`?(\w+)`?\s*\([^)]+\)\s+VALUES\s*([^;]+);'
            matches = re.findall(insert_pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            
            self.stdout.write(f'Found {len(matches)} INSERT statements')
            
            imported_count = 0
            for table_name, values_block in matches:
                # Skip if it's not the right table format
                if table_name not in ['table60b', 'calculator_vcftable']:
                    continue
                
                # Split the values block into individual value tuples
                # Remove newlines and extra spaces
                values_block = re.sub(r'\s+', ' ', values_block.strip())
                
                # Extract individual value tuples
                value_tuples = re.findall(r'\(([^)]+)\)', values_block)
                
                self.stdout.write(f'Found {len(value_tuples)} value tuples in {table_name}')
                
                for values_str in value_tuples:
                    values = values_str.split(',')
                    if len(values) >= 3:
                        try:
                            # Handle different column orders based on table format
                            if table_name == 'table60b':
                                # Format: (id, density, temperature, vcf, class, vcf2)
                                density = float(values[1].strip().strip("'"))
                                temperature = float(values[2].strip().strip("'"))
                                vcf = float(values[3].strip().strip("'"))
                            else:
                                # Format: (density, temperature, vcf)
                                density = float(values[0].strip().strip("'"))
                                temperature = float(values[1].strip().strip("'"))
                                vcf = float(values[2].strip().strip("'"))

                            # Create VCF entry
                            VCFTable.objects.get_or_create(
                                density=density,
                                temperature=temperature,
                                defaults={'vcf': vcf}
                            )
                            imported_count += 1

                        except (ValueError, IndexError) as e:
                            self.stdout.write(
                                self.style.WARNING(f'Skipping invalid data: {values_str} - {e}')
                            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {imported_count} VCF entries.')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing VCF data: {e}')
            )

        # Alternative method using raw SQL if the above doesn't work
        # Uncomment the following if you need to execute raw SQL
        """
        try:
            with open(sql_file, 'r') as file:
                sql_content = file.read()
            
            with connection.cursor() as cursor:
                cursor.execute(sql_content)
            
            self.stdout.write(
                self.style.SUCCESS('VCF data imported successfully using raw SQL.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error executing raw SQL: {e}')
            )
        """ 