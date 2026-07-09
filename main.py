from app2 import PyFremioApp

app = PyFremioApp()

@app.route("/home")
def home(request, response) -> None: 
    response.text = "Hello from Home"

@app.route("/about")
def about(request, response):
    response.text = "Hello from About"

@app.route("/show/{name}")
def root(request, response, name):
    response.text = f"Hello, {name}"