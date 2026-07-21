# PyFremio

A minimal Python **WSGI web framework** built on top of [WebOb](https://webob.org/).
It gives you routing, class-based handlers, Jinja2 templates, static-file serving,
middleware and a small response helper — in a tiny, easy-to-read codebase.

## Features

- 🧭 **Routing** with dynamic path parameters (`/hello/{name}`)
- 🎛️ **Per-route allowed methods** (`allowed_methods=["get", "post"]`)
- 🧱 **Function- and class-based handlers**
- 🖼️ **Jinja2 templates** out of the box
- 📁 **Static files** served via [WhiteNoise](https://whitenoise.readthedocs.io/)
- 🔌 **Middleware** support
- 🧪 **Built-in test client** backed by `requests`
- 🧯 **Custom exception handler**
- 📦 **Response helpers** for `text`, `html` and `json`

## Installation

```bash
pip install pyfremio
```

## Quick start

Create an `app.py`:

```python
from pyfremio import PyFremioApp

app = PyFremioApp()


@app.route("/home", allowed_methods=["get"])
def home(request, response):
    response.text = "Hello from Home"


@app.route("/hello/{name}")
def greet(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/json")
def as_json(request, response):
    response.json = {"framework": "PyFremio"}


@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "List of books"

    def post(self, request, response):
        response.text = "Created a book"
```

Run it with any WSGI server, e.g. [Gunicorn](https://gunicorn.org/):

```bash
pip install gunicorn
gunicorn app:app
```

Then open http://127.0.0.1:8000/hello/world

## Templates

By default templates are loaded from a `templates/` directory:

```python
@app.route("/home-template")
def home_template(request, response):
    response.html = app.template(
        "index.html",
        context={"title": "PyFremio", "body": "Welcome!"},
    )
```

Configure the directory when creating the app:

```python
app = PyFremioApp(templates_dir="templates", static_dir="static")
```

## Static files

Any file placed in the `static/` directory is served automatically by WhiteNoise,
for example `static/main.css` is available at `/static/main.css`.

## Middleware

```python
from pyfremio import Middleware


class LoggingMiddleware(Middleware):
    def process_request(self, req):
        print("request:", req.path)

    def process_response(self, req, res):
        print("response:", res.status_code)


app.add_middleware(LoggingMiddleware)
```

## Exception handling

```python
def on_error(request, response):
    response.text = "Something went wrong"


app.add_exception_handler(on_error)
```

## Testing

PyFremio ships a `requests`-based test client:

```python
def test_home():
    client = app.test_session()
    response = client.get("http://testserver/home")
    assert response.text == "Hello from Home"
```

## License

MIT
