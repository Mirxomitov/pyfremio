from webob import Request, Response 

class PyFremioApp:
    def __init__(self) -> None:
        self.routes = dict()

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)
    
    def handle_request(self, request):
        response = Response()

        for path, ketmon in self.routes.items():
            if path == request.path:
                ketmon(request, response)
                return response

        self.default_response(response)
        return response
        
    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found"

    def route(self, path):
        def teshavoy(ketmon):
            self.routes[path] = ketmon
            return ketmon

        return teshavoy
