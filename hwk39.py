from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

app = FastAPI(
    title="Music Product API",
    description="API for managing musical products",
)

products_db = [
    {
        "name": "Marshall Headphones",
        "price": 200.0,
        "discount_price": 8.0,
        "quantity": 100,
        "category": "Headphones",
        "sku": "MARSH123",
        "email": "marshall@example.com",
        "stock": True
    },
    {
        "name": "Sony Headphones",
        "price": 150.0,
        "discount_price": 5.0,
        "quantity": 50,
        "category": "Headphones",
        "sku": "SONY456",
        "email": "sony@example.com",
        "stock": True
    },
    {
        "name": "Bose Headphones",
        "price": 300.0,
        "discount_price": 10.0,
        "quantity": 30,
        "category": "Headphones",
        "sku": "BOSE789",
        "email": "bose@example.com",
        "stock": False
    },
    {
        "name": "JBL Headphones",
        "price": 250.0,
        "discount_price": 15.0,
        "quantity": 20,
        "category": "Headphones",
        "sku": "JBL012",
        "email": "jbl@example.com",
        "stock": True
    },
    {
        "name": "Audiotechnica Vinyl Player",
        "price": 400.0,
        "discount_price": 20.0,
        "quantity": 10,
        "category": "Vinyl Players",
        "sku": "AUDIO345",
        "email": "audio@example.com",
        "stock": True
    }

]

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    discount_price: float | None = Field(default=None, gt=0)
    quantity: int = Field(ge=0)
    category: str
    sku: str = Field(min_length=3, max_length=10)
    email: EmailStr
    stock: bool = True

    @field_validator("name")
    @classmethod
    def name_formatter(cls, value):
        return value.strip()

    @field_validator("sku")
    @classmethod
    def sku_validator(cls, value):
        if " " in value or not value.isupper():
            raise ValueError("SKU must be uppercase and cannot contain spaces")
        return value

    @model_validator(mode="after")
    def discount_price_validator(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("Discount price must be less than the regular price")
        return self


class ProductResponse(BaseModel):
    name: str
    price: float
    discount_price: float | None
    quantity: int
    category: str
    stock: bool

@app.post("/products/", response_model=ProductResponse)
def create_product(product: Product):
    products_db.append(product.dict())
    return product

@app.get("/products/", response_model=list[ProductResponse])
def get_products():
    return products_db
