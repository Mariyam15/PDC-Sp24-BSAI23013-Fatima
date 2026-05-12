# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time

app = FastAPI()


@app.middleware("http")
async def add_student_id_header(request, call_next):

    response = await call_next(request)

    response.headers["X-Student-ID"] = "BSAI23013"

    return response

failure_count = 0
circuit_open = False
MAX_FAILURES = 3

def call_llm():

    # Simulate slow API
    time.sleep(10)

    # Simulate failure
    raise Exception("LLM API Failed")


@app.get("/generate")
def generate_text():

    global failure_count
    global circuit_open

    # If circuit breaker is open
    if circuit_open:

        return JSONResponse(
            content={
                "message": "Circuit Open - Using fallback response"
            }
        )

    try:

        call_llm()

        return {
            "message": "LLM Success"
        }

    except Exception:

        failure_count += 1

        print(f"Failure Count: {failure_count}")

        # Open circuit after repeated failures
        if failure_count >= MAX_FAILURES:

            circuit_open = True

            print("Circuit Breaker OPENED")

        return JSONResponse(
            content={
                "message": "LLM Failed - Fallback Response Returned"
            }
        )
