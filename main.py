from fastapi import FastAPI, Depends
from models import Product
from database import SessionLocal, engine
import db_models
from sqlalchemy.orm import Session

app = FastAPI()

# Create tables in PostgreSQL
db_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def wish():
    return "Hey welcome to the inventory!"

# Sample Data
products = [
    Product(
        id=1,
        name="iphone",
        description="1tb storage",
        price=100,
        quantity=12
    ),
    Product(
        id=2,
        name="headset",
        description="fastrack new model",
        price=120,
        quantity=10
    )
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Insert sample data into database
def init_db():
    db = SessionLocal()

    count = db.query(db_models.Product).count()  # Fixed

    if count == 0:
        for product in products:
            db.add(db_models.Product(**product.model_dump()))

        db.commit()

    db.close()

# init_db()


# Show all products
@app.get("/products")
def show_products(db: Session = Depends(get_db)):
    db_products = db.query(db_models.Product).all()
    return db_products


# Get product by ID
@app.get("/product/{id}")
def get_product_by_id(id: int , db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
            return db_product

    return {"message": "Product not found"}


@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):

    db_product = db_models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {
        "message": "Product added successfully",
        "product": db_product
    }

# Update product
@app.put("/product/{id}")
def update_product(id: int, product: Product , db: Session = Depends(get_db)):
         db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
         if db_product:
              
              db_product.name = product.name
              db_product.description = product.description
              db_product.price = product.price
              db_product.quantity = product.quantity
              db.commit()     
              db.refresh(db_product)
              return{
                   "message":"product updated Successfullly",
                   "Product": db_product
              }         
         else :
                return " No product found"
    

# Delete product
@app.delete("/product/{id}")
def delete_product(id: int , db: Session = Depends(get_db)):

    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
         db.delete(db_product)
         db.commit()
    else :
         return "Product not found"