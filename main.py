from app import PyFremioApp

app = PyFremioApp()

@app.route("/home")
def home(request, response) -> None: 
    response.text = "Hello from Home"

@app.route("/about")
def about(request, response):
    response.text = "Hello from About"

@app.route("/")
def root(request, response):
    response.text = "Hello"