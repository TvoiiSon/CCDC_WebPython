import os
from CCDCServer.urls import Url
from view import HomePage, EpicMath, Hello, LoginPage

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATE_DIR_NAME': 'templates'
}

urlpatterns = [
    Url('^$', HomePage),
    Url('^/login$', LoginPage),
    Url('^/math$', EpicMath),
    Url('^/hello$', Hello)
]
