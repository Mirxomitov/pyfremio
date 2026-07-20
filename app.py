from typing import Any

from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter
import os
from jinja2 import FileSystemLoader, Environment
from whitenoise import WhiteNoise
from constants import ALL_HTTP_METHODS
from middleware import Middleware

class PyFremioApp:
    def __init__(self, templates_dir="templates", static_dir="static") -> None:
        self.routes = {}
        self.template_env = Environment(
            loader = FileSystemLoader(os.path.abspath(templates_dir))
        )
        self.exception_handler = None
        self.middleware = LoggingMiddleware(self)
        self.whitenoise = WhiteNoise(self.middleware, root=static_dir)

    def __call__(self, environ, start_response) -> Any:
        return self.whitenoise(environ, start_response)
    
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler_data, kwargs = self.find_handler(request.path)

        if handler_data is None:
            response.status_code = 404
            response.text = "Not found"
            return response

        handler = handler_data["handler"]
        allowed_methods = handler_data["allowed_methods"]
        
        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)

        if handler is None or request.method.lower() not in allowed_methods:
            response.status_code = 405
            response.text = "Method not allowed"
            return response

        try:
            handler(request, response, **kwargs)  # type: ignore
        except Exception:
            if self.exception_handler is None:
                raise

            response.status_code = 500
            self.exception_handler(request, response)

        return response
    
    def find_handler(self, path):
        for p, handler_data in self.routes.items():
            parsed_path = parse(p, path)
            
            if parsed_path is not None:
                return handler_data, parsed_path.named

        return None, None
        

    def route(self, path, allowed_methods=[]):
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods)
            return handler
        
        return wrapper
    
    def add_route(self, path, handler, allowed_methods=[]):
        assert path not in self.routes, f"Duplicate path {path}"
        
        if not allowed_methods:
            allowed_methods = ALL_HTTP_METHODS
        
        self.routes[path] = {"handler" : handler, "allowed_methods": allowed_methods}
    
    def test_session(self):
        session = requests.Session()
        session.mount('http://testserver', wsgiadapter.WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        template = self.template_env.get_template(name=template_name).render(**context)
        return template.encode()
    
    def add_exception_handler(self, handler):
        self.exception_handler = handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

class LoggingMiddleware (Middleware):
    def __init__(self, app):
        super().__init__(app)
    
    def process_request(self, req):
        print("request is called ")
    
    def process_response(self, req, res):
        print("response is called")