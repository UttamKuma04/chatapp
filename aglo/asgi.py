# aglo/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aglo.settings')

# Initialize Django first
django_asgi_app = get_asgi_application()

# Now safely import routing (which may load models, consumers, etc.)
import app.routing  

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
})
