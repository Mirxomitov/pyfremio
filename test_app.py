import pytest
from app import PyFremioApp

def test_basic_route_adding(app):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello from home"

def test_duplicate_route(app):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello from home"   

    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req, res):
            res.text = "Hello from home"
    
def test_requests_can_be_sent_by_test_client(app, test_client):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello from Home"

    response = test_client.get("http://testserver/home")
    assert response.text == "Hello from Home"

def test_route_with_param(app, test_client):
    @app.route("/hello/{name}")
    def hello(req, res, name):
        res.text = f"Hello {name}"

    assert test_client.get("http://testserver/hello/Tohir").text == "Hello Tohir"
    assert test_client.get("http://testserver/hello/Jahongir").text == "Hello Jahongir"

def test_default_response (test_client):
    response = test_client.get("http://testserver/nonexistingpage")
    assert response.status_code == 404
    assert response.text == "Not found"

def test_class_based_request_get(app, test_client):
    @app.route("/books")
    class Books:
        def get(self, request, response):
            response.text = "get books"

    assert test_client.get("http://testserver/books").text == "get books"

def test_class_based_request_post(app, test_client):
    @app.route("/books")
    class Books:
        def post(self, request, response):
            response.text = "Endpoint post books"
    
    assert test_client.post("http://testserver/books").text == "Endpoint post books"

def test_class_based_method_not_allowed(app, test_client):
    @app.route("/books")
    class Books:
        def get(self, request, response):
            response.text = "get books"
    
    response = test_client.post("http://testserver/books")
    
    assert response.status_code == 405
    assert response.text == "Method not allowed"

def test_alternative_route_adding(app):
    def handler(req, res):
        res.text = "Alternative route adding"

    app.add_route("home", handler)

def test_template_handler(app, test_client):
    @app.route("/test-template")
    def test_template(req, res):
        res.body = app.template(
            "test.html",
            context={"new_title": "New Title", "new_body": "New Body"}
        )

    response = test_client.get("http://testserver/test-template")

    assert "New Title" in response.text
    assert "New Body" in response.text
    assert "text/html" in response.headers["Content-Type"]

def test_template_without_context(app):
    content = app.template("test.html")

    assert isinstance(content, bytes)

def test_exception_handler(app, test_client):
    def on_exception(req, res):
         res.text= "Something bad happened"
    
    app.add_exception_handler(on_exception)

    @app.route("/exception")
    def exception_throwing(req, res):
        raise AssertionError("some exception")
    

    response = test_client.get("http://testserver/exception")

    assert response.text == "Something bad happened"

def test_static_file_not_found(test_client):
    assert test_client.get("http://testserver/nonexistant.css").status_code == 404


def test_static_file(test_client):
    response =  test_client.get("http://testserver/test.css")

    assert response.text == "body { background-color: chocolate;}"