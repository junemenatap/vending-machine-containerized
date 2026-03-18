from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import VendingDatabase
from schemas import Products

app = FastAPI()
db = VendingDatabase()
db.create_tables()

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
    return db.get_all_products()

@app.post("/products")
def add_product(Product: Products):
    db.add_item(Product.name, Product.price)
    return {"message": f"{Product.name} added successfully"}

@app.delete("/products/{name}")
def delete_product(name: str):
    try:
        db.delete_item(name)
        return {"message": f"{name} deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
    
@app.patch("/products/{name}")
def update_product_price(name: str, new_price: int):
    try:
        db.update_item_price(name, new_price)
        return {"message": f"{name} price updated successfully"}
    except Exception as e:
        return {"error": str(e)}