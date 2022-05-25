import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_chale_hum.settings")

application = get_asgi_application()
