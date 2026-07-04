from fastapi import FastAPI , HTTPException
from db_pratice import Base, engine
from Pratice_model import ProductPratice
from fastapi import Depends
from db_pratice import session
from sqlalchemy.orm import Session
from schema_pydantic import ProductCreate

app = FastAPI()

@app.get("/")

def home():
        return "Hello Inventory Api"

def get_db():
        db = session()
        try:
            yield db
        finally:
            db.close()    

Base.metadata.create_all(bind=engine)  

@app.post("/products")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = ProductPratice(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products")
def get_product(
      db : Session = Depends(get_db)

):
      products = db.query(ProductPratice).all()
      return products

@app.get("/products/{product_id}")
def get_product(product_id :int , db:Session = Depends(get_db)):
      product = db.query(ProductPratice).filter(ProductPratice.id == product_id).first()
      if not product:
            raise HTTPException(status_code = 404 , detail = "Product not found")
      return product
#update the product

@app.put("/products/{product_id}")
def get_product(product_id : int , product_data , db : Session = Depends(get_db)):
      product = db.query(ProductPratice).filter(ProductPratice.id == product_id).first()
      if not product:
            raise HTTPException(status_code = 404 , detail = "product not found:")
      product.name = product_data.name
      product.description = product_data.description
      product.price = product_data.price
      product.quantity = product_data.quantity
      db.commit()
      db.refresh(product)
      return product

#delete the product
@app.delete("/products/{product_id}")
def delete_product(product_id : int , db:Session = Depends(get_db)):
      product = db.query(ProductPratice).filter(ProductPratice.id == product_id).first()
      if not product:
            raise HTTPException(status_code = 404 , detail = "Product not found:")
      
      db.delete(product)
      db.commit()
      return {"message": "product deleted Successfully:"}