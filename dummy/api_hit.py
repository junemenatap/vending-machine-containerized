from fastapi import FastAPI
import asyncio
import random

app = FastAPI()

@app.get("/ping")
async def ping():
    # Simulate a random delay with log-normal distribution ~75% below 500 ms, ~91% below 2 seconds
    await asyncio.sleep(random.lognormvariate(-2.2, 2.2))
    if random.random() < 0.005:  # 0.5% chance to simulate an error
        raise Exception("Simulated error")
    return {"status": "ok"}
