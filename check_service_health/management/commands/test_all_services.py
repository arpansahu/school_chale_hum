# check_service_health/management/commands/test_all_services.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from io import StringIO


class Command(BaseCommand):
    help = 'Run all service health checks for the School Chale Hum application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed output for each service'
        )
        parser.add_argument(
            '--skip',
            nargs='+',
            type=str,
            metavar='SERVICE',
            help='Skip specific services (e.g., --skip storage email)'
        )
        parser.add_argument(
            '--only',
            nargs='+',
            type=str,
            metavar='SERVICE',
            help='Only check specific services (e.g., --only db cache)'
        )

    def handle(self, *args, **options):
        verbose = options.get('detailed', False)
        skip_services = options.get('skip') or []
        only_services = options.get('only')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(
            '   🏥 SCHOOL CHALE HUM - SERVICE HEALTH CHECK'
        ))
        self.stdout.write('='*70 + '\n')
        
        # Define all available services
        all_services = [
            ('db', 'test_db', 'Database (PostgreSQL)', True),
            ('cache', 'test_cache', 'Cache (Redis)', True),
            ('storage', 'test_storage', 'Storage (MinIO/S3)', getattr(settings, 'USE_S3', False)),
            ('email', 'test_email', 'Email Service (MailJet)', self._is_email_configured()),
        ]
        
        # Filter services based on arguments
        services_to_check = []
        for key, command, name, is_configured in all_services:
            if only_services:
                if key in only_services:
                    services_to_check.append((key, command, name, is_configured))
            elif key not in skip_services:
                services_to_check.append((key, command, name, is_configured))
        
        results = {}
        
        for key, command, service_name, is_configured in services_to_check:
            self.stdout.write(f'{"-"*70}')
            
            if not is_configured:
                self.stdout.write(self.style.WARNING(f'⏭️  {service_name}: SKIPPED (not configured)'))
                results[service_name] = '⏭️  SKIPPED'
                continue
            
            self.stdout.write(self.style.HTTP_INFO(f'🔍 Testing: {service_name}'))
            self.stdout.write(f'{"-"*70}')
            
            out = StringIO()
            err = StringIO()
            
            try:
                # Build command arguments
                cmd_kwargs = {'stdout': out, 'stderr': err}
                if verbose:
                    cmd_kwargs['verbosity'] = 2
                
                call_command(command, **cmd_kwargs)
                output = out.getvalue()
                error = err.getvalue()
                
                if error:
                    self.stdout.write(self.style.ERROR(error))
                    results[service_name] = '❌ FAILED'
                elif 'ERROR' in output.upper() or 'FAILED' in output.upper() or '❌' in output:
                    self.stdout.write(output)
                    results[service_name] = '❌ FAILED'
                elif '⚠️' in output or 'WARNING' in output.upper():
                    self.stdout.write(output)
                    results[service_name] = '⚠️  WARNING'
                else:
                    self.stdout.write(output)
                    results[service_name] = '✅ PASSED'
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error running {command}: {e}'))
                results[service_name] = '❌ ERROR'
        
        # Print summary
        self.stdout.write(f'\n{"="*70}')
        self.stdout.write(self.style.SUCCESS('   📊 SERVICE HEALTH CHECK SUMMARY'))
        self.stdout.write(f'{"="*70}\n')
        
        for service_name, status in results.items():
            self.stdout.write(f'   {service_name:.<50} {status}')
        
        self.stdout.write(f'\n{"="*70}\n')
        
        # Determine overall status
        failed = sum(1 for status in results.values() if '❌' in status)
        warnings = sum(1 for status in results.values() if '⚠️' in status)
        passed = sum(1 for status in results.values() if '✅' in status)
        skipped = sum(1 for status in results.values() if '⏭️' in status)
        
        total = len(results)
        
        if failed > 0:
            self.stdout.write(self.style.ERROR(
                f'   ❌ {failed}/{total} service(s) FAILED, '
                f'{warnings} warning(s), {passed} passed, {skipped} skipped'
            ))
        elif warnings > 0:
            self.stdout.write(self.style.WARNING(
                f'   ⚠️  {warnings}/{total} service(s) have warnings, '
                f'{passed} passed, {skipped} skipped'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'   ✅ All {passed}/{total} configured service(s) are healthy! '
                f'({skipped} skipped)'
            ))
        
        self.stdout.write(f'{"="*70}\n')
    
    def _is_email_configured(self):
        """Check if email is configured"""
        return bool(
            getattr(settings, 'MAIL_JET_API_KEY', None) and
            getattr(settings, 'MAIL_JET_API_SECRET', None)
        )
