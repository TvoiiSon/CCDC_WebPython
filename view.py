from datetime import datetime
from CCDCServer.view import View
from CCDCServer.request import Request
from CCDCServer.response import Response
from CCDCServer.redirect import Redirect
from CCDCServer.models import Authentication
from CCDCServer.template import LoadTemplate
from CCDCServer.middleware import Session
import jinja2


class HomePage(View):
    def get(self, request, *args, **kwargs):
        if not request.session_id:
            return Redirect(request, location="/login")

        template_loader = jinja2.FileSystemLoader(searchpath="templates")
        jinja_env = jinja2.Environment(loader=template_loader)
        template = jinja_env.get_template("home.html")
        context = {'time': str(datetime.now()), 'lst': [1, 2, 3], 'test': request.session_id}
        html_content = template.render(context)
        return Response(request, body=html_content)


class LoginPage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        html_content = LoadTemplate(template_folder="templates", template_name="login.html").load_template()

        return Response(request, body=str(html_content))

    def post(self, request: Request, *args, **kwargs) -> Response:
        login = request.POST.get('login', '')[0]
        password = request.POST.get('password', '')[0]
        model_auth = Authentication(login, password).auth()
        if model_auth:
            response = Redirect(request, location="/")
            session_middleware = Session()
            session_middleware.to_response(response)
            return response
        else:
            html_content = LoadTemplate(template_folder="templates", template_name="login.html").load_template()

            return Response(request, body=html_content)


class RegistrationPage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        html_content = LoadTemplate(template_folder="templates", template_name="registration.html").load_template()

        return Response(request, body=html_content)

    def post(self, request: Request, *args, **kwargs) -> Response:
        login = request.POST.get('login', '')[0]
        password = request.POST.get('password', '')[0]
        model_auth = Authentication(login, password).reg()
        if model_auth:
            return Redirect(request, location="/login")
        else:
            html_content = LoadTemplate(template_folder="templates", template_name="registration.html").load_template()

            return Response(request, body=html_content)


class EpicMath(View):
    pass
    # def get(self, request: Request, *args, **kwargs):
    #     first = request.GET.get('first')
    #     if not first or not first[0].isnumeric():
    #         return Response(request, body=f'first пустое либо не является числом')
    #
    #     second = request.GET.get('second')
    #     if not second or not second[0].isnumeric():
    #         return Response(request, body=f'second пустое либо не является числом')
    #
    #     return Response(request, body=f'Сумма {first[0]} и {second[0]} равна {int(first[0]) + int(second[0])}')


class Hello(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        template_loader = jinja2.FileSystemLoader(searchpath="templates")
        jinja_env = jinja2.Environment(loader=template_loader)
        template = jinja_env.get_template("hello.html")
        html_content = template.render()

        return Response(request, body=html_content)
