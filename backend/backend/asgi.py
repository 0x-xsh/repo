
import os

from django.core.asgi import get_asgi_application
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter ##new

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

import api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
	'http': asgi_application,
	'websocket':
	
	
			URLRouter(api.routing.websocket_urlpatterns)
		
	
})