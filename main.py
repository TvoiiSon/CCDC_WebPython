from CCDCServer.main import CCDCServer
from CCDCServer.middleware import middlewares
from setting import settings, urlpatterns

app = CCDCServer(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares
)
