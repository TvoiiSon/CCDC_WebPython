from CCDCServer.urls import Url
from view import HomePage, EpicMath, Hello, LoginPage


urlpatterns = [
    Url('^$', HomePage),
    Url('^/login$', LoginPage),
    Url('^/math$', EpicMath),
    Url('^/hello$', Hello)
]
