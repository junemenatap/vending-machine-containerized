from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import VendingDatabase
from schemas import Products
import requests
import logging

app = FastAPI()
db = VendingDatabase()
db.create_tables()

logger = logging.getLogger("uvicorn.error")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/products")
def read_products():
    try:
        requests.get("http://dummy:9000/ping", timeout=5)
    except requests.exceptions.RequestException as err:
        logger.error(f"API hit to dummy service failed: {err}")
    try:
        return db.get_all_products()
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {err}")

@app.post("/products")
def add_product(Product: Products):
    try:
        db.add_item(Product.name, Product.price)
        return {"message": f"{Product.name} added successfully"}
    except Exception as err:
        logger.error(f"Error adding product: {err}")
        raise HTTPException(status_code=500, detail=f"Error adding product: {err}")

@app.delete("/products/{name}")
def delete_product(name: str):
    try:
        db.delete_item(name)
        return {"message": f"{name} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting product: {e}")

@app.patch("/products/{name}")
def update_product_price(name: str, new_price: int):
    try:
        db.update_item_price(name, new_price)
        return {"message": f"{name} price updated successfully"}
    except Exception as e:
        logger.error(f"Error updating product price: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating product price: {e}")

# INTENTIONALLY VULNERABLE - no locking
@app.post("/products/buy/{name}")
def buy_item(name: str):
    try:
        stock = db.get_stock(name)  # READ
        if stock > 0:
            db.decrement_stock(name)  # WRITE

            product = db.get_product(name)

            try:
                receipt_response = requests.post("http://receipt:3000/receipt", json={
                    "name": product['name'],
                    "price": product['price'],
                    "amount": 1,
                }, timeout=3)
                receipt = receipt_response.json().get("receipt", "")
            except requests.exceptions.RequestException as err:
                logger.error(f"API hit to receipt service failed: {err}")
                receipt = "Receipt service unavailable."
            return {"message": f"{name} purchased successfully", "receipt": receipt}
        return {"error": f"{name} is out of stock"}
    except Exception as err:
        logger.error(f"Error buying product: {err}")
        raise HTTPException(status_code=500, detail=f"Error buying product: {err}")

@app.patch("/products/{name}/replenish")
def replenish_product(name: str, amount: int = 5000):
    try:
        db.replenish_stock(name, amount)
        return {"message": f"{name} restocked by {amount}"}
    except Exception as e:
        logger.error(f"Error replenishing product: {e}")
        raise HTTPException(status_code=500, detail=f"Error replenishing product: {e}")