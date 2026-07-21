import json
from webob import Response as WebResponse

class Response:
    def __init__(self) -> None:
        self.content_type = None
        self.status_code = 200

        self.html = None
        self.text = ""
        self.json = None
        self.body = b''

    def set_body_and_content_type(self):
        
        if self.html is not None:
            self.body = self.html
            self.content_type = "text/html"

        if self.text:
            self.body = self.text
            self.content_type = "text/plain"

        if self.json is not None:
            self.body = json.dumps(self.json).encode()
            self.content_type = "application/json"

    def __call__(self, environ, start_response):
        self.set_body_and_content_type()

        response = WebResponse(
            body=self.body,
            content_type=self.content_type,
            status=self.status_code,
        )

        return response(environ, start_response)
    
