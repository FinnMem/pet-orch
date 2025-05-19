from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import random

app = FastAPI()

# 🔢 Базовые метрики
REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")

# 📈 Кастомные метрики
JOBS_DISPATCHED = Counter("petorch_jobs_dispatched_total", "Total jobs dispatched")
JOBS_SUCCESS = Counter("petorch_jobs_success_total", "Total successful jobs")
JOBS_FAILURE = Counter("petorch_jobs_failure_total", "Total failed jobs")
JOB_DURATION = Histogram("petorch_job_duration_seconds", "Job processing duration")

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

@app.post("/run-job")
def run_job():
    JOBS_DISPATCHED.inc()
    start_time = time.time()
    
    try:
        # 🎲 Симуляция работы: 0.1–1.5 сек
        duration = random.uniform(0.1, 1.5)
        time.sleep(duration)

        # 🎯 Успех или неудача случайным образом
        if random.random() < 0.8:
            JOBS_SUCCESS.inc()
            return {"status": "success", "duration": duration}
        else:
            raise Exception("Simulated job failure")
    except Exception as e:
        JOBS_FAILURE.inc()
        return {"status": "failure", "error": str(e)}
    finally:
        JOB_DURATION.observe(time.time() - start_time)