import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "22f3000713@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-d37inn.example.com"

app = FastAPI()

# CORS: only this exact origin is allowed.
# Never use "*" for this assignment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# This runs for EVERY request: GET, OPTIONS, errors, etc.
@app.middleware("http")
async def add_required_headers(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{max(process_time, 0):.6f}"

    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        numbers = [int(x.strip()) for x in values.split(",") if x.strip() != ""]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must be comma-separated integers"},
        )

    if len(numbers) == 0:
        return JSONResponse(
            status_code=400,
            content={"error": "values must contain at least one integer"},
        )

    count = len(numbers)
    total = sum(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    mean = total / count

    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": mean,
    }
