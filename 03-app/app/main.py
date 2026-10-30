import subprocess

from fastapi import FastAPI, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.api_route("/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def hello(request: Request):
    if request.method == "POST" and request.headers.get("Test") == "Hello":
        return Response("Hello, World!")
    return Response(status_code=403)

@app.get("/health")
def health():
    ok = subprocess.run(["ping", "-c", "1", "-W", "2", "77.88.8.8"]).returncode == 0
    return Response("OK" if ok else "FAIL", status_code=200 if ok else 503)
