from typing import Any

from webob import Request, Response
from parse import parse
import inspect

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
            return response
        

        if kwargs is not None:
            handler(request, response, **kwargs)

        handler(request, response)

        return response
    
    def find_handler(self, path):
        for p, handler in self.routes.items():
            parsed_path = parse(p, path)
            
            if parsed_path is not None:
                return handler, parsed_path.named

        return None, None
        

    def route(self, path):
        assert path not in self.routes, f"Duplicate path {path}"

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper