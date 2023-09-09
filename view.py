from datetime import datetime
from CCDCServer.view import View
from CCDCServer.request import Request
from CCDCServer.response import Response
from CCDCServer.template_engine import build_template
from CCDCServer.redirect import Redirect


class HomePage(View):
    def get(self, request, *args, **kwargs):
        # if not request.session_id:
        #     from setting import settings, urlpatterns
        #     redirect = Redirect(urls=urlpatterns, url='/login', settings=settings)
        #     redirect.invoke()
        body = build_template(
            request,
            {'time': str(datetime.now()), 'lst': [1, 2, 3], 'test': request.session_id},
            'home.html'
        )
        return Response(request, body=body)


class LoginPage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(
            request,
            {'error_cookie': 'Auth!'},
            'login.page.html'
        )

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass


class EpicMath(View):
    def get(self, request: Request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(request, body=f'first пустое либо не является числом')

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return Response(request, body=f'second пустое либо не является числом')

        return Response(request, body=f'Сумма {first[0]} и {second[0]} равна {int(first[0]) + int(second[0])}')


class Hello(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'name': 'undefind'}, 'hello.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        raw_name = request.POST.get('answer')
        name = raw_name[0] if raw_name else 'undefind'
        body = build_template(request, {'name': name}, 'hello.html')

        return Response(request, body=body)
