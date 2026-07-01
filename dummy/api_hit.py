from fastapi import FastAPI
import asyncio
import random

app = FastAPI()

@app.get("/ping")
async def ping():
    # Simulate a random delay between 0.05 and 2 seconds
    await asyncio.sleep(random.uniform(0.05, 2))
    if random.random() < 0.005:  # 0.5% chance to simulate an error
        raise Exception("Simulated error")
    return {"status": "ok"}
