# check_service_health/management/commands/test_email.py

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Test if email service (MailJet) is configured and working properly'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed output'
        )
        parser.add_argument(
            '--send-test',
            type=str,
            metavar='EMAIL',
            help='Send a test email to this address'
        )

    def handle(self, *args, **options):
        verbose = options.get('detailed', False)
        test_email = options.get('send_test')
        
        self.stdout.write(self.style.WARNING('Testing MailJet Email configuration...'))
        
        # 1. Check MailJet API settings
        self.stdout.write('Checking MailJet API settings...')
        
        mailjet_api_key = getattr(settings, 'MAIL_JET_API_KEY', None)
        mailjet_secret_key = getattr(settings, 'MAIL_JET_API_SECRET', None)
        mailjet_email = getattr(settings, 'MAIL_JET_EMAIL_ADDRESS', None)
        
        if verbose:
            self.stdout.write(f'     API Key: {mailjet_api_key[:10]}***' if mailjet_api_key else '     API Key: Not set')
            self.stdout.write(f'     Secret Key: {mailjet_secret_key[:5]}***' if mailjet_secret_key else '     Secret Key: Not set')
            self.stdout.write(f'     Email Address: {mailjet_email}' if mailjet_email else '     Email Address: Not set')
        
        # Validate settings
        issues = []
        
        if not mailjet_api_key:
            issues.append('MAIL_JET_API_KEY is not configured')
        
        if not mailjet_secret_key:
            issues.append('MAIL_JET_API_SECRET is not configured')
            
        if not mailjet_email:
            issues.append('MAIL_JET_EMAIL_ADDRESS is not configured')
        
        if issues:
            self.stdout.write(self.style.ERROR('  ❌ MailJet configuration issues:'))
            for issue in issues:
                self.stdout.write(self.style.ERROR(f'     - {issue}'))
            return
        
        self.stdout.write(self.style.SUCCESS('  ✅ MailJet API credentials configured'))
        
        # 2. Test MailJet API connection
        self.stdout.write('Testing MailJet API connection...')
        
        try:
            from mailjet_rest import Client
            
            mailjet = Client(
                auth=(mailjet_api_key, mailjet_secret_key),
                version='v3'
            )
            
            # Get account info / sender list
            result = mailjet.sender.get()
            
            if result.status_code == 200:
                self.stdout.write(self.style.SUCCESS('  ✅ MailJet API connection successful'))
                
                senders = result.json().get('Data', [])
                if verbose and senders:
                    self.stdout.write(f'     Found {len(senders)} verified sender(s):')
                    for sender in senders[:5]:
                        status = '✅' if sender.get('Status') == 'Active' else '⚠️'
                        self.stdout.write(f'       {status} {sender.get("Email")}')
                elif senders:
                    active_senders = [s for s in senders if s.get('Status') == 'Active']
                    self.stdout.write(self.style.SUCCESS(f'  ✅ Found {len(active_senders)} active sender(s)'))
                else:
                    self.stdout.write(self.style.WARNING('  ⚠️  No verified senders found'))
            else:
                self.stdout.write(self.style.ERROR(
                    f'  ❌ MailJet API returned status {result.status_code}'
                ))
                if verbose:
                    self.stdout.write(f'     Response: {result.json()}')
                return
                
        except ImportError:
            self.stdout.write(self.style.ERROR(
                '  ❌ mailjet-rest package not installed. Run: pip install mailjet-rest'
            ))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ MailJet API error: {e}'))
            return
        
        # 3. Send test email if requested
        if test_email:
            self.stdout.write(f'\nSending test email to {test_email}...')
            try:
                data = {
                    'Messages': [
                        {
                            "From": {
                                "Email": mailjet_email,
                                "Name": "School Chale Hum Health Check"
                            },
                            "To": [
                                {
                                    "Email": test_email,
                                    "Name": "Recipient"
                                }
                            ],
                            "Subject": "Email Service Health Check",
                            "TextPart": "This is a test email from School Chale Hum health check system.",
                            "HTMLPart": "<h3>Email Service Health Check</h3><p>This is a test email from School Chale Hum health check system.</p>"
                        }
                    ]
                }
                
                mailjet = Client(auth=(mailjet_api_key, mailjet_secret_key), version='v3.1')
                result = mailjet.send.create(data=data)
                
                if result.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f'  ✅ Test email sent successfully to {test_email}'))
                else:
                    self.stdout.write(self.style.ERROR(f'  ❌ Failed to send email. Status: {result.status_code}'))
                    if verbose:
                        self.stdout.write(f'     Response: {result.json()}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error sending test email: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Email service test completed'))
