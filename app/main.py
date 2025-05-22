from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
import time
import random

from app.api import routes  # импортируем твой router

app = FastAPI()

# Подключаем роутер с корневым маршрутом "/"
app.include_router(routes.router)

# Автоматическая инициализация базовых метрик FastAPI
Instrumentator().instrument(app).expose(app)

# Кастомные метрики
JOBS_DISPATCHED = Counter("petorch_jobs_dispatched_total", "Total jobs dispatched")
JOBS_SUCCESS = Counter("petorch_jobs_success_total", "Total successful jobs")
JOBS_FAILURE = Counter("petorch_jobs_failure_total", "Total failed jobs")
JOB_DURATION = Histogram("petorch_job_duration_seconds", "Job processing duration")

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": time.time()}

@app.post("/run-job")
def run_job():
    JOBS_DISPATCHED.inc()
    start_time = time.time()

    try:
        duration = random.uniform(0.1, 1.5)
        time.sleep(duration)

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
