from fastapi import FastAPI, HTTPException
import asyncio
import random

app = FastAPI()

@app.get("/ping")
async def ping():
    # Simulate a random delay with log-normal distribution ~81% below 500 ms, ~96% below 2 seconds
    await asyncio.sleep(random.lognormvariate(-2, 1.5))
    if random.random() < 0.005:  # 0.5% chance to simulate an error
        raise HTTPException(status_code=500, detail="Simulated server error")
    return {"status": "ok"}
