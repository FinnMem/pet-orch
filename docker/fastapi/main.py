from fastapi import FastAPI
import time
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")

@app.get("/")
def read_root():
    REQUEST_COUNT.inc()
    return {"message": "Hello, DevOps!"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": time.time()}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
