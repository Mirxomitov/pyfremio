from app import PyFremioApp
from middleware import Middleware

app = PyFremioApp()

@app.route("/home", allowed_methods=["get"])
def home(request, response) -> None: 
    response.text = "Hello from Home"

@app.route("/about")
def about(request, response):
    response.text = "Hello from About"

@app.route("/hello/{name}")
def root(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "hello"

    def post(self, request, response):
        response.text = "Endpoint post books"

@app.route("/home-template")
def home_template(req, res):
    res.html = app.template(
        "test.html",
        context={"new_title": "Tohir's Python Framework", "new_body": "New Body"}
    )

@app.route("/json")
def json(req, res):
    res.json = {"name": "Pyfremio"}