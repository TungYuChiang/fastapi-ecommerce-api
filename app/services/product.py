from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductSchema


def create_product(db: Session, product: ProductSchema) -> Product:
    new_product = Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def get_product(db: Session, product_id: int) -> Product:
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(db: Session, product_id: int, product: ProductSchema) -> Product:
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if existing_product:
        existing_product.name = product.name
        existing_product.description = product.description
        existing_product.price = product.price
        db.commit()
        db.refresh(existing_product)
    return existing_product


def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False
