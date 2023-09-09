import os
from CCDCServer.main import CCDCServer
from urls import urlpatterns
from CCDCServer.middleware import middlewares

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATE_DIR_NAME': 'templates'
}

app = CCDCServer(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares
)