from typing import Any

from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter

class PyFremioApp:
    def __init__(self) -> None:
        self.routes = {}
    
    def __call__(self, environ, start_response) -> Any:
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

        handler(request, response, **kwargs)

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
