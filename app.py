from typing import Any

from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter
import os
from jinja2 import FileSystemLoader, Environment
from whitenoise import WhiteNoise

class PyFremioApp:
    def __init__(self, templates_dir="templates", static_dir="static") -> None:
        self.routes = {}
        self.template_env = Environment(
            loader = FileSystemLoader(os.path.abspath(templates_dir))
        )
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
    
    def __call__(self, environ, start_response) -> Any:
        return self.whitenoise(environ, start_response)
    
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is None:
            response.status_code = 404
            response.text = "Not found"
            return response
        
        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)

        if handler is None:
            response.status_code = 405
            response.text = "Method not allowed"
            return response

        try:
            handler(request, response, **kwargs) # type: ignore
        except Exception:
            if self.exception_handler is None:
                raise

            response.status_code = 500
            self.exception_handler(request, response)

        return response
    
    def find_handler(self, path):
        for p, handler in self.routes.items():
            parsed_path = parse(p, path)
            
            if parsed_path is not None:
                return handler, parsed_path.named

        return None, None
        

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        
        return wrapper
    
    def add_route(self, path, handler):
        assert path not in self.routes, f"Duplicate path {path}"
        self.routes[path] = handler
    
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
